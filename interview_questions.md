# L2 GCP Data Engineer — Interview Questions + Expected Answers (GCP)

Scope: **GCS, BigQuery, Airflow, PySpark/Spark on Dataproc, Dataflow** + SQL, data modeling, reliability, and behavioral ownership.

---

## Q1 — Design: Batch ingestion from GCS to BigQuery (idempotent + late files)
**Question:**  
Daily vendor files land in **GCS** for multiple entities; files can be **duplicated**, arrive **late by up to 2 days**, and sometimes require **backfills**. Describe the end-to-end design you would use to ingest into **BigQuery curated tables**, and explain how your approach keeps results correct on retries/reruns, handles late arrivals without double counting, and supports backfilling past dates safely.

**Expected answer (complete):**
- Uses an **immutable raw/landing zone** in GCS (never overwrite raw), with a predictable path convention (source/entity/date/batch) and basic governance (IAM, logging, retention).
- Loads into **BigQuery staging** with lineage fields (e.g., file name/URI, load timestamp, batch/run identifier, ingestion date).
- Produces **curated** tables with explicit **grain** and a deterministic strategy for applying changes:
  - **MERGE/upsert** keyed on business keys when receiving incrementals/changes, or
  - **partition overwrite** when a “full daily snapshot” is the contract.
- Ensures **idempotency** by making reruns deterministic: same input partition(s) produce the same curated state, no matter how many times the run is replayed.
- Handles late data via a clear policy (e.g., reprocess a rolling window of partitions or scoped MERGEs) and reconciliation checks to detect corrections.
- Supports backfills by parameterizing the run date/range and writing only the impacted partitions/keys, with concurrency controls to avoid overwhelming BQ.

**What to listen for (strong signals):**
- Mentions **grain + keys**, deterministic dedupe, and “curated only changes via a controlled publish.”
- Calls out **late-arrival window** and why it limits cost and risk.
- Mentions **auditability** (metadata tables / processed file inventory) and basic **DQ gates**.

---

## Q2 — Data modeling: Facts, dimensions, and grain control (avoid double counting)
**Question:**  
You’re building an analytics model in BigQuery for **users, orders, order_items, and payments** that will be queried by BI tools. Propose the tables you would create, clearly state the **grain** of each, and explain how your model prevents **double counting** when analysts join across orders, items, and payment attempts.

**Expected answer (complete):**
- Separates grains into appropriate facts:
  - `fact_orders`: **1 row per order_id**
  - `fact_order_items`: **1 row per (order_id, line_id/sku)**
  - `fact_payment_attempts`: **1 row per payment attempt/payment_id** (often many per order)
- Dimensions like `dim_user`, `dim_product`, `dim_date` (and optionally SCD2 for changing attributes).
- Prevents double counting by:
  - Defining metric ownership (e.g., revenue from items; payment attempts not directly joined to orders for revenue unless rolled up).
  - Requiring pre-aggregation/rollups when joining facts with different grains (e.g., roll payments to 1 row/order before joining to `fact_orders`).
- BigQuery physical design awareness: partition facts by event/order date, cluster on join/filter keys.

**What to listen for (strong signals):**
- Explicitly says “**don’t mix grains**,” and explains the fanout risk in plain language.
- Knows when to compute order totals vs item totals (and how to reconcile).

---

## Q3 — Logic/debug: Revenue doubled after joining payments
**Question:**  
A report joined `orders` to `payments` and overnight the reported **revenue doubled** without a real business change. Explain the most likely root cause, how you would correct the logic so the join can’t inflate metrics, and how you would validate the fix.

**Expected answer (complete):**
- Identifies **join fanout** as the likely cause (one order to many payment attempts/retries), multiplying order rows.
- Fixes by aligning grain before joining:
  - roll up payments to **one row per order** (success flag, first success timestamp, etc.), or
  - use a semi-join pattern conceptually (filter orders to those with a successful payment) rather than bringing many payment rows into the result.
- Validates with:
  - uniqueness checks at each grain,
  - row-count comparisons pre/post join,
  - reconciliation against a trusted revenue definition (often item rollups).

**What to listen for (strong signals):**
- Talks about **cardinality** and shows a repeatable validation approach, not just a one-off fix.

---

## Q4 — Logic/SQL fundamentals: Window functions and determinism
**Question:**  
You need a curated table that keeps only the **latest event per `event_id`** from a large stream of records, but you’ve seen cases where two records have the same timestamp and the “latest” record changes between runs. Describe the logic you would use to make the result **deterministic**, and explain the trade-offs at scale in BigQuery or Spark.

**Expected answer (complete):**
- Uses a window function (`row_number`) over `event_id` ordered by:
  - primary: event timestamp descending
  - tie-breaker: a stable unique field (e.g., ingestion timestamp + source_file + sequence id) to guarantee determinism.
- Acknowledges scale trade-offs:
  - windowing causes shuffle/sort by key; can be expensive.
  - suggests incremental processing patterns when possible (process only new/changed keys; partitioning strategies; careful reprocessing window for late updates).
- Explains how to validate correctness (duplicate key checks; sampling tie cases; invariants).

**What to listen for (strong signals):**
- Mentions a **tie-breaker** (this is where many candidates fail).
- Understands that “correct” and “fast” can conflict and proposes pragmatic mitigations.

---

## Q5 — BigQuery performance & cost: Bytes scanned increased 10×
**Question:**  
A BigQuery query that used to scan ~200GB now scans ~2TB and is 10× slower. Describe how you would diagnose the change using BigQuery job details/query plan, the most common reasons this happens, and how you would fix it while keeping results correct.

**Expected answer (complete):**
- Starts with evidence: bytes processed, stage breakdown, shuffle/spill indicators, and whether partition pruning occurred.
- Common causes and fixes:
  - lost **partition pruning** (missing/ineffective partition filter, wrong column, function-wrapped predicate) → rewrite predicates, enforce required partition filters
  - `SELECT *` / pulling wide nested fields → project only needed columns, avoid unnecessary UNNEST
  - join explosion / duplicated join keys → dedupe/pre-aggregate, validate cardinality
  - UNNEST blow-up → unnest only when needed and after filtering
- Mentions cost governance options (materialization, summary tables/materialized views where appropriate, workload management).

**What to listen for (strong signals):**
- Explains pruning in plain terms and knows how it gets accidentally disabled.
- Calls out join explosion as both a correctness and cost risk.

---

## Q6 — Spark/Dataproc performance: Shuffle, skew, and stable runtimes
**Question:**  
A PySpark job on **Dataproc** is unstable: some runs finish in 20 minutes, others take 2 hours, mostly during joins and aggregations. Explain how you would isolate the cause (including skew), what changes you would make to reduce shuffle and stabilize runtime, and how you would confirm improvement.

**Expected answer (complete):**
- Uses Spark UI/metrics to identify where time is spent (shuffle read/write, skewed tasks, spill).
- Reduces data early (filter and select columns) and pre-aggregates where possible before joins.
- Uses broadcast joins appropriately for small dimensions and avoids unnecessary repartitions.
- Addresses skew explicitly (hot keys): salting, isolating heavy-key population, two-phase aggregation, or alternate join strategies.
- Confirms improvement with before/after metrics (shuffle volume, task skew distribution, runtime variance), not just one successful run.

**What to listen for (strong signals):**
- Talks about **variance** and skew, not just average runtime.
- Proposes a verification method (metrics) rather than “it should be faster.”

---

## Q7 — Architecture choice: Dataflow vs Dataproc (batch + streaming late data)
**Question:**  
You need to implement two pipelines: (1) a batch ETL pipeline and (2) a streaming pipeline with **late-arriving events** and event-time semantics. Explain when you would choose **Dataflow** vs **Dataproc**, and justify your choice based on operational ownership, correctness needs, and team realities.

**Expected answer (complete):**
- For streaming with late events: often prefers **Dataflow** due to first-class event-time handling (windowing/watermarks/triggers) and managed operations (autoscaling, checkpointing).
- For batch ETL: chooses based on existing ecosystem and needs:
  - **Dataproc** when Spark/library reuse, complex Spark transformations, or runtime control matters
  - **Dataflow** when standardizing on Beam and minimizing cluster ops is valued
- Recognizes trade-offs: ops burden, cost model, skills, connector maturity, and debugging practices.

**What to listen for (strong signals):**
- Mentions **event time + late data** explicitly (not just “streaming service vs batch service”).
- Gives pragmatic reasons tied to the team and operating model.

---

## Q8 — Design: Airflow orchestration that supports retries, reruns, backfills, and no partial publishes
**Question:**  
Your Airflow DAG orchestrates daily ingestion from **GCS to BigQuery curated tables**, but failures and retries sometimes create duplicates or leave downstream users seeing partially updated data. Describe the DAG design you would implement to ensure **safe retries**, **safe reruns/backfills**, and **no partial publishes**, including how you’d gate downstream consumption and what validations you’d require before data is considered “ready.”

**Expected answer (complete):**
- Uses a “**publish gate**” pattern: curated tables become visible/usable only when the run has fully succeeded and validations pass.
- Makes tasks rerunnable by design: staging loads are scoped to the run/partition; curated updates are deterministic (MERGE keyed on business keys or partition overwrite scoped to run date).
- Prevents partial publish by:
  - concentrating curated writes into a controlled publish operation (not many ad hoc appends), and
  - gating consumption via a partition readiness signal (control table/flag or downstream dependency on a “ready” marker).
- Includes practical validations:
  - schema/contract checks on ingest,
  - duplicate key checks at curated grain,
  - basic reconciliation totals and freshness checks,
  - alerting with run context.

**What to listen for (strong signals):**
- Explicitly describes how downstream users/jobs avoid reading half-baked partitions.
- Understands idempotency at both staging and curated layers.

---

## Q9 — Behavioral: Production incident ownership
**Question:**  
Tell me about a production data incident you owned (bad data published, missed SLA, or a pipeline outage). Explain what the impact was, how you stabilized the situation, how you communicated with stakeholders, what the root cause was, and what you changed so it wouldn’t happen again.

**Expected answer (complete):**
- Clear impact assessment (who was affected, how severe, what was wrong).
- Demonstrates ownership: containment (pause downstream / stop publish), restores service safely, communicates updates with a cadence.
- Root cause based on evidence (not guesses), e.g., schema drift, join fanout, missing partition filter, late data policy gap.
- Preventative controls added: DQ gates, alerts, runbooks, schema validation/contract, idempotent publish improvements, postmortem with actions and owners.

**What to listen for (strong signals):**
- Balanced technical and communication response.
- “Fix + prevention,” not just a heroic one-time recovery.

---

## Q10 — Behavioral: Cross-team schema changes and conflict management
**Question:**  
An upstream team changes a schema and your pipeline breaks right before a reporting deadline. Explain how you would handle the immediate problem and how you would work with the upstream team afterward so breaking changes don’t keep recurring.

**Expected answer (complete):**
- Immediate response prioritizes safety and correctness: pause publish or rollback; implement a compatible hotfix only if safe.
- Post-incident prevention focuses on:
  - data contract/versioning and deprecation windows,
  - automated schema validation and quarantine,
  - shared pre-release validation/testing process,
  - clear ownership and escalation paths only when needed.
- Maintains a collaborative tone and aligns on shared SLAs.

