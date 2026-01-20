"""
pdf_ingest_rag.py

Purpose:
- Extract clean text and table data from PDF files
- Normalize into chunks suitable for RAG (text chunks, table row chunks, table-summary chunks)
- Compute embeddings using sentence-transformers
- Persist documents + embeddings + metadata into a Chroma vector store for retrieval

Functions:
- extract_pdf_structured(pdf_path) -> dict of {'text': [...], 'tables': [...]}
- chunk_text(text, chunk_size=1000, overlap=200) -> list[str]
- normalize_table(table_rows) -> (headers, data_rows)
- table_to_chunks(headers, data_rows, rows_per_chunk=5) -> list[str] with metadata per chunk
- ingest_pdf_to_chroma(pdf_path, collection_name, chroma_dir, embed_model_name)
"""

from pathlib import Path
from typing import List, Dict, Any, Tuple
import pdfplumber
import uuid
import os
import time
import json

# Embedding & vector DB
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings

# ---------------------------
# Utilities
# ---------------------------
def _safe_text(cell) -> str:
    if cell is None:
        return ""
    if isinstance(cell, str):
        return " ".join(cell.split())
    return str(cell)

def _make_unique_headers(headers: List[str]) -> List[str]:
    seen = {}
    out = []
    for i, h in enumerate(headers):
        key = h.strip() if isinstance(h, str) and h.strip() != "" else f"Column_{i+1}"
        if key in seen:
            seen[key] += 1
            out.append(f"{key}_{seen[key]}")
        else:
            seen[key] = 0
            out.append(key)
    return out

def _is_header_candidate(row: List[str]) -> bool:
    non_empty = [c for c in row if c not in (None, "")]
    if not non_empty:
        return False
    alpha_like = sum(1 for c in non_empty if any(ch.isalpha() for ch in c))
    return alpha_like >= max(1, len(non_empty) / 2)

def _normalize_table_rows(table: List[List[Any]]) -> Tuple[List[str], List[List[str]]]:
    """
    Ensure correct header detection and row padding.
    Returns (headers, data_rows)
    """
    # Clean cells and filter empty rows (but keep rows that may be all empty? we drop fully empty)
    rows = [[_safe_text(c) for c in r] for r in table]
    # Drop rows that are fully empty
    rows = [r for r in rows if any(cell.strip() != "" for cell in r)]
    if not rows:
        return [], []

    max_cols = max(len(r) for r in rows)
    padded = [r + [""] * (max_cols - len(r)) for r in rows]

    first_row = padded[0]
    if _is_header_candidate(first_row):
        headers_raw = [h if h.strip() != "" else f"Column_{i+1}" for i, h in enumerate(first_row)]
        headers = _make_unique_headers(headers_raw)
        data_rows = padded[1:]
    else:
        # no header row detected -> create default headers
        headers = [f"Column_{i+1}" for i in range(max_cols)]
        data_rows = padded

    # ensure rows are same length as headers
    data_rows = [r + [""] * (len(headers) - len(r)) if len(r) < len(headers) else r for r in data_rows]
    return headers, data_rows

# ---------------------------
# Extraction: text + tables (pdfplumber)
# ---------------------------
def extract_pdf_structured(pdf_path: str, pages: str = "all", debug: bool = False) -> Dict[str, Any]:
    """
    Extract structured content from PDF using pdfplumber:
      - text: list of {page:int, text:str}
      - tables: list of {page:int, table_index:int, headers:[...], rows:[[...]], data_records:[{header:cell}]}

    Note: We use pdfplumber here for portability. If Camelot is preferred for table accuracy,
    you can replace the table extraction with Camelot and then apply the same normalization.
    """
    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        raise FileNotFoundError(f"{pdf_path} not found")

    result = {"text": [], "tables": []}
    with pdfplumber.open(pdf_path) as pdf:
        num_pages = len(pdf.pages)
        # pages parameter support: "all" or "1-3,5"
        page_nums = []
        if pages == "all":
            page_nums = list(range(1, num_pages + 1))
        else:
            # allow simple page range string like "1-3" or "5"
            for part in str(pages).split(","):
                part = part.strip()
                if "-" in part:
                    a,b = part.split("-",1)
                    page_nums.extend(range(int(a), int(b)+1))
                else:
                    page_nums.append(int(part))

        for pnum in page_nums:
            if pnum < 1 or pnum > num_pages:
                continue
            page = pdf.pages[pnum-1]
            # Extract text block cleaned
            text = page.extract_text()
            if text and text.strip() != "":
                cleaned = " ".join(text.split())
                result["text"].append({"doc": pdf_path.name, "page": pnum, "text": cleaned})

            # Extract tables: pdfplumber returns list-of-rows
            tables = page.extract_tables()
            for t_idx, table in enumerate(tables, start=1):
                # table may be None or empty
                if not table or len(table) == 0:
                    continue
                headers, data_rows = _normalize_table_rows(table)
                if not headers:
                    continue
                records = [dict(zip(headers, row)) for row in data_rows]
                result["tables"].append({
                    "doc": pdf_path.name,
                    "page": pnum,
                    "table_index": t_idx,
                    "headers": headers,
                    "rows": data_rows,
                    "data_records": records
                })
                if debug:
                    print(f"[page {pnum} table {t_idx}] headers={headers} rows={len(data_rows)}")
    return result

# ---------------------------
# Chunking
# ---------------------------
def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
    """Chunk long text into overlapping chunks of approx chunk_size characters."""
    if not text:
        return []
    text = text.strip()
    chunks = []
    start = 0
    length = len(text)
    while start < length:
        end = start + chunk_size
        chunks.append(text[start:end].strip())
        start += chunk_size - overlap
    return chunks

def table_rows_to_chunks(headers: List[str], rows: List[List[str]], rows_per_chunk: int = 5) -> List[Tuple[str, List[int]]]:
    """
    Convert table rows into textual chunks.
    Returns list of (chunk_text, row_indices_in_original_table)
    Each chunk_text is a human-readable representation of rows:
      e.g. "Row 1: ColumnA=..., ColumnB=...; Row 2: ..."
    """
    if not headers or not rows:
        return []
    chunks = []
    total_rows = len(rows)
    for i in range(0, total_rows, rows_per_chunk):
        block_rows = rows[i:i+rows_per_chunk]
        row_indices = list(range(i, min(i+rows_per_chunk, total_rows)))
        lines = []
        for r_idx, row in zip(row_indices, block_rows):
            pairs = [f"{h}={_safe_text(cell)}" for h, cell in zip(headers, row)]
            lines.append(f"ROW_{r_idx+1}: " + " | ".join(pairs))
        chunks.append(("\n".join(lines), row_indices))
    return chunks

# ---------------------------
# Embedding + Chroma persistence
# ---------------------------
def init_chroma_client(persist_dir: str = "./chroma_db") -> Any:
    os.makedirs(persist_dir, exist_ok=True)
    client = chromadb.Client(Settings(
        chroma_db_impl="duckdb+parquet",
        persist_directory=persist_dir
    ))
    return client

def create_or_get_collection(client, name: str):
    try:
        return client.create_collection(name=name)
    except Exception:
        return client.get_collection(name=name)

def embed_texts(embedder, texts: List[str]) -> List[List[float]]:
    # sentence-transformers returns numpy arrays, convert to list for Chroma
    embs = embedder.encode(texts, convert_to_numpy=True)
    return embs.tolist()

# ---------------------------
# Top-level ingest function
# ---------------------------
def ingest_pdf_to_chroma(pdf_path: str,
                         collection_name: str = "dq_docs",
                         persist_dir: str = "./chroma_db",
                         embed_model_name: str = "all-MiniLM-L6-v2",
                         chunk_size: int = 1000,
                         chunk_overlap: int = 200,
                         rows_per_table_chunk: int = 4,
                         pages: str = "all",
                         debug: bool = False) -> Dict[str, Any]:
    """
    Ingest the pdf into a local Chroma collection.
    Returns a summary dict with counts.
    """

    start_ts = time.time()
    pdf_path = str(pdf_path)
    # 1) extract structured content
    structured = extract_pdf_structured(pdf_path, pages=pages, debug=debug)

    # 2) init embedder and chroma
    embedder = SentenceTransformer(embed_model_name)
    client = init_chroma_client(persist_dir)
    collection = create_or_get_collection(client, collection_name)

    docs_to_add = []
    metadatas = []
    ids = []

    # 3) text chunks -> documents
    doc_counter = 0
    for t in structured.get("text", []):
        doc_name = t.get("doc")
        page = t.get("page")
        text = t.get("text", "")
        chunks = chunk_text(text, chunk_size=chunk_size, overlap=chunk_overlap)
        for idx, ch in enumerate(chunks):
            doc_id = f"{Path(pdf_path).stem}_text_p{page}_c{idx}_{uuid.uuid4().hex[:8]}"
            docs_to_add.append(ch)
            metadatas.append({
                "source": doc_name,
                "type": "text",
                "page": page,
                "chunk_index": idx
            })
            ids.append(doc_id)
            doc_counter += 1

    # 4) table chunks -> documents (row blocks)
    table_counter = 0
    for table in structured.get("tables", []):
        doc_name = table.get("doc")
        page = table.get("page")
        t_idx = table.get("table_index")
        headers = table.get("headers", [])
        rows = table.get("rows", [])
        # table-level summary chunk (optional) - useful for retrieving table as a whole
        summary_text = f"TABLE_SUMMARY: page={page} table_index={t_idx} headers={headers} num_rows={len(rows)}"
        id_summary = f"{Path(pdf_path).stem}_table_p{page}_t{t_idx}_summary_{uuid.uuid4().hex[:8]}"
        docs_to_add.append(summary_text)
        metadatas.append({
            "source": doc_name,
            "type": "table_summary",
            "page": page,
            "table_index": t_idx,
            "headers": headers,
            "num_rows": len(rows)
        })
        ids.append(id_summary)
        table_counter += 1

        chunks = table_rows_to_chunks(headers, rows, rows_per_chunk=rows_per_table_chunk)
        for c_idx, (chunk_text, row_indices) in enumerate(chunks):
            doc_id = f"{Path(pdf_path).stem}_table_p{page}_t{t_idx}_r{row_indices[0]}_{uuid.uuid4().hex[:8]}"
            docs_to_add.append(chunk_text)
            metadatas.append({
                "source": doc_name,
                "type": "table_rows",
                "page": page,
                "table_index": t_idx,
                "headers": headers,
                "row_indices": row_indices
            })
            ids.append(doc_id)
            table_counter += 1

    # 5) Embedding in batches
    batch_size = 64
    total = len(docs_to_add)
    if total == 0:
        return {"status": "no_docs", "ingested": 0}

    if debug:
        print(f"Embedding {total} documents using model {embed_model_name}")

    for i in range(0, total, batch_size):
        batch_docs = docs_to_add[i:i+batch_size]
        batch_ids = ids[i:i+batch_size]
        batch_meta = metadatas[i:i+batch_size]
        embs = embed_texts(embedder, batch_docs)
        # add to collection (Chroma)
        collection.add(ids=batch_ids, documents=batch_docs, metadatas=batch_meta, embeddings=embs)
        if debug:
            print(f"Added batch {i}..{i+len(batch_docs)-1}")

    client.persist()
    elapsed = time.time() - start_ts
    return {
        "status": "ok",
        "ingested_text_chunks": doc_counter,
        "ingested_table_chunks": table_counter,
        "total_documents": total,
        "elapsed_seconds": elapsed,
        "collection_name": collection_name,
        "persist_directory": persist_dir
    }

# ---------------------------
# Example usage (run as script)
# ---------------------------
if __name__ == "__main__":
    # Change these to your environment
    PDF_PATH = r"C:\Users\prkumarsharma\Desktop\dq\FR_2052a20220429_f.pdf"
    COLLECTION_NAME = "dq_docs"
    CHROMA_DIR = "./chroma_db"
    EMBED_MODEL = "all-MiniLM-L6-v2"  # lightweight local model

    summary = ingest_pdf_to_chroma(
        pdf_path=PDF_PATH,
        collection_name=COLLECTION_NAME,
        persist_dir=CHROMA_DIR,
        embed_model_name=EMBED_MODEL,
        chunk_size=1200,
        chunk_overlap=200,
        rows_per_table_chunk=4,
        pages="all",
        debug=True
    )
    print("\nINGEST SUMMARY:")
    print(json.dumps(summary, indent=2))
