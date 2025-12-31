# NL2SQL-Compiler

**A Compiler-Based, Deterministic, and Verifiable Natural Language to SQL System**

---

## 1. Motivation

Natural Language to SQL (NL2SQL) systems have existed for years, yet **most remain fundamentally unreliable**.

Despite impressive demonstrations using large language models (LLMs), current NL2SQL approaches suffer from persistent and well-known failures:

* Hallucinated tables and columns
* Non-deterministic SQL generation
* No formal correctness guarantees
* Poor explainability
* No security or governance model
* Tight coupling between language models and execution logic

In short:

> **Most NL2SQL systems are demos, not systems.**

This project exists to address that gap.

---

## 2. Core Philosophy

This project is built on a **single, non-negotiable principle**:

> **Natural language should not be translated directly into SQL.**

Instead, NL2SQL must be treated as a **compilation problem**, not a text generation problem.

### Compiler Analogy

Just as modern compilers do not translate source code directly into machine code, we do **not** translate natural language directly into SQL.

Instead, we introduce a **validated semantic intermediate representation (IR)**.

```
Natural Language
   ↓
Semantic Intermediate Representation (IR)
   ↓
Schema-Constrained Validation
   ↓
Deterministic SQL Compilation
```

This architectural decision is the foundation of the system’s **correctness, explainability, and novelty**.

---

## 3. What This Project Is (and Is Not)

### This project **is**:

* A **compiler-based NL2SQL system**
* Deterministic and reproducible
* Schema-aware by construction
* Explainable without post-hoc LLM text
* Designed for correctness before convenience
* Fully open-source

### This project **is not**:

* A prompt-engineering demo
* An LLM wrapper that “hopes” SQL is correct
* A black-box agent system
* A proprietary API-dependent tool

---

## 4. Architectural Overview

### High-Level Pipeline

```
User Input (Natural Language)
        ↓
(Optional) LLM-based NL → IR Mapping
        ↓
Semantic IR Validation
        ↓
Deterministic SQL Compiler
        ↓
SQL Output (Execution optional)
```

**Important:**
There is **no direct NL → SQL path** anywhere in the system.

---

## 5. Semantic Intermediate Representation (IR)

The **Semantic IR** is the heart of the system.

It explicitly represents **what the user intends**, independent of SQL syntax.

### Example IR

```json
{
  "intent": "aggregation",
  "tables": ["orders"],
  "metrics": [
    { "column": "orders.amount", "operation": "SUM" }
  ],
  "dimensions": ["orders.customer_id"],
  "filters": [],
  "joins": []
}
```

### Why This Matters

The IR enables:

* Formal validation against database schema
* Deterministic SQL generation
* Natural-language explanations derived from structure
* Rejection of hallucinations **before SQL exists**
* Cross-database portability
* Security and policy enforcement at compile time

This IR is **explicit, typed, and validated** — not implicit reasoning hidden inside an LLM.

---

## 6. Schema-Aware Validation

Before SQL is ever produced, the IR is validated against the **actual database schema** using SQLAlchemy introspection.

Validation includes:

* Table existence
* Column existence
* Correct table.column references
* Structural consistency

If validation fails, the system **refuses to generate SQL**.

This is deliberate.

> Incorrect queries should fail loudly, not execute silently.

---

## 7. Deterministic SQL Compilation

SQL is **compiled**, not generated.

Given the same IR, the compiler will always produce the same SQL string.

### Example Output

```sql
SELECT SUM(orders.amount)
FROM orders
GROUP BY orders.customer_id
```

Properties:

* No randomness
* No hallucination
* Fully testable
* Fully explainable
* Fully reproducible

---

## 8. Current Project Status (What Is Implemented)

As of now, the system includes:

### Implemented Components

* Semantic IR (Pydantic-based)
* Schema introspection (SQLite, extensible)
* IR validation engine
* Deterministic SQL compiler
* FastAPI-based API
* End-to-end pipeline: IR → SQL
* Working example database
* Manual and programmatic testing via API

### Supported SQL Features (v0.1)

* `SELECT`
* `WHERE`
* `GROUP BY`
* Aggregations (`SUM`, `COUNT`, `AVG`, `MIN`, `MAX`)
* Single-table queries

### Explicitly Out of Scope (for now)

* Subqueries
* Window functions
* `INSERT / UPDATE / DELETE`
* Query execution
* Cost-based optimization

These exclusions are **intentional** to preserve correctness guarantees.

---

## 9. Reproducibility Guide

### 9.1 Requirements

* Python ≥ 3.11
* SQLite (default)
* Windows / Linux / macOS

### 9.2 Installation

```bash
git clone <repo-url>
cd nl2sql-compiler
pip install -e .
```

### 9.3 Create Example Database

```sql
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    name TEXT
);

CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    amount REAL,
    order_date TEXT,
    FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
);
```

Save as:

```
examples/db.sqlite
```

### 9.4 Run the API

```bash
uvicorn app.main:app --reload
```

Visit:

```
http://127.0.0.1:8000/docs
```

### 9.5 Test Query

```json
POST /query
{
  "intent": "aggregation",
  "tables": ["orders"],
  "metrics": [
    { "column": "orders.amount", "operation": "SUM" }
  ],
  "dimensions": ["orders.customer_id"],
  "filters": [],
  "joins": []
}
```

---

## 10. Why This Is Novel

This project is novel **not because of LLM usage**, but because of **what it refuses to do**.

### Key Novel Contributions

1. **Mandatory Semantic IR**

   * No bypass allowed
2. **Schema-Constrained Validation Before SQL**

   * Hallucination-free by construction
3. **Deterministic SQL Compilation**

   * Same IR → same SQL
4. **Explainability from Structure**

   * No post-hoc LLM explanations
5. **Compiler-Based Framing**

   * Treats NL2SQL as a systems problem, not a language trick

To our knowledge, **no open-source NL2SQL system integrates all of these properties end-to-end**.

---

## 11. Future Roadmap

### Short-Term (Next Milestones)

* Harden validation rules (joins, types, GROUP BY correctness)
* Canonical SQL formatting
* Negative test cases
* Expanded SQLite + PostgreSQL support

### Mid-Term

* NL → IR mapping using JSON-constrained LLM output
* Ambiguity detection and clarification loop
* Role-based access and security policies
* IR-based query explanation generation

### Long-Term

* Cost-aware query planning
* Cross-database IR portability
* Formal evaluation on Spider / WikiSQL
* Academic publication
* Production hardening

---

## 12. Design Constraints (Read Before Contributing)

* SQL must **never** be generated by an LLM
* IR validation must always precede compilation
* Determinism is mandatory
* Correctness > coverage
* Fail fast, fail explicitly

If a contribution violates these constraints, it will not be accepted.

---

## 13. License

Apache License 2.0
Free for research, commercial use, and modification.

---

## 14. Final Note

This project is intentionally opinionated.

It is built for people who believe that:

* Systems should be correct by design
* Explainability is a feature, not an afterthought
* LLMs should assist, not replace, formal reasoning

If that resonates with you, you are in the right place.

---

