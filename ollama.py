import pdfplumber  # PyMuPDF
import requests
import json
from pathlib import Path
from textwrap import dedent

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "phi3"


def extract_pdf_text(pdf_path):
    """Extract all text from a PDF file."""
    text=[]
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text.append(page.extract_text() or "")
    return "\n".join(text)


def query_ollama(prompt: str, model: str = MODEL_NAME) -> str:
    """Send a prompt to Ollama and return the response."""
    payload = {"model": model, "prompt": prompt}
    response = requests.post(OLLAMA_URL, json=payload, stream=True)

    output = ""
    for line in response.iter_lines():
        if line:
            data = json.loads(line.decode("utf-8"))
            if "response" in data:
                output += data["response"]
            if data.get("done", False):
                break
    return output.strip()


def generate_dq_cases(rules_pdf, mapping_pdf, template_pdf, output_file="dq_test_cases.md"):
    # Step 1: Extract text
    rules_text = extract_pdf_text(rules_pdf)
    mapping_text = extract_pdf_text(mapping_pdf)
    template_text = extract_pdf_text(template_pdf)

    # Step 2: Build master prompt
    prompt = dedent(f"""
    You are a senior Data Quality Engineer.
    Task:
     Summarise {rules_text[:10000]}.
     Do not write any code.
    """)

    # Step 3: Query Ollama
    dq_cases = query_ollama(prompt)

    # Step 4: Save output
    Path(output_file).write_text(dq_cases, encoding="utf-8")
    print(f"✅ DQ Test Cases generated in {output_file}")


if __name__ == "__main__":
    generate_dq_cases(
        rules_pdf=r"C:\Users\prkumarsharma\Desktop\dq\FR_2052a20220429_f.pdf",
        mapping_pdf=r"C:\Users\prkumarsharma\Desktop\dq\data_requirements.pdf",
        template_pdf=r"C:\Users\prkumarsharma\Desktop\dq\DQTemplate.pdf",
        output_file=r"C:\Users\prkumarsharma\Desktop\dq\dq_test_cases.md"
    )
    #rules_pdf = r"C:\Users\prkumarsharma\Desktop\dq\FR_2052a20220429_f.pdf"
    #pdf = extract_pdf_text(rules_pdf)
    #print(pdf)