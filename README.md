# Askbase — Natural Language Analytics Engine

Askbase lets you query any PostgreSQL database using plain English.
No SQL knowledge required. Just ask a question and get results instantly.

Built as an AI systems engineering project, Askbase goes far beyond a simple LLM wrapper. It combines dynamic schema intelligence, vector memory, and automatic error recovery into a full analytics pipeline.

---

## How It Works

You type a question like _"show top 5 customers by total spending"_.

Askbase automatically extracts your database schema, infers relationships between tables using foreign keys and naming patterns, retrieves semantically similar past queries from vector memory, builds a schema-aware prompt, sends it to a Groq-hosted LLM, executes the generated SQL against your PostgreSQL database, and returns structured results — all in seconds.

```
User question
      ↓
Schema extraction + ER inference
      ↓
RAG memory retrieval (similar past queries)
      ↓
Schema-aware prompt construction
      ↓
Groq LLM → SQL generation
      ↓
Safety check (block dangerous queries)
      ↓
Execute against PostgreSQL
      ↓
Failed? → Automatic SQL repair loop (up to 2 retries)
      ↓
Return results + store successful query in memory
```

---

## Key Features

**Natural Language to SQL**
Converts plain English questions into executable PostgreSQL queries using Groq LLMs with schema-grounded prompting. No hardcoded table names — the system adapts to any database structure.

**Dynamic Schema Extraction**
Automatically inspects any connected database and extracts tables, columns, data types, primary keys, and foreign keys without any manual configuration.

**ER Relationship Inference**
Builds entity relationships from both explicit foreign keys and inferred naming patterns (e.g. `orders.customer_id → customers.id`), helping the AI understand how to join tables correctly.

**RAG Query Memory**
Stores successful question and SQL pairs as vector embeddings using sentence-transformers. On each new question, retrieves semantically similar past queries and injects them into the prompt — making the system smarter over time with every successful query.

**Automatic SQL Repair Loop**
If a generated query fails, the error message is sent back to the LLM which attempts to fix the SQL automatically, retrying up to 2 times before giving up. Only repaired and verified SQL enters the system.

**Security**
Blocks dangerous queries containing DROP, DELETE, TRUNCATE, ALTER, and UPDATE before execution reaches the database.

**Clean React Frontend**
Two-panel UI — live schema browser on the left, query interface on the right. Shows generated SQL, execution time, row count, and results table. Includes example query suggestions.

---

## Queries Tested

The following query categories have been tested against a sample e-commerce database (customers, orders, products tables).

| Category | Example Query | Status |
|---|---|---|
| Basic fetch | show all customers | ✅ Works |
| Filtering | show customers from mumbai | ✅ Works |
| Aggregation | show total revenue per customer | ✅ Works |
| Sorting | show total spending per customer sorted by highest first | ✅ Works |
| Single JOIN | show products bought by each customer | ✅ Works |
| LEFT JOIN | show customers who never placed an order | ✅ Works |
| GROUP BY + HAVING | show customers who ordered more than 3 products | ✅ Works |
| Multi-table analytics | show top 5 customers by total spending | ✅ Works |
| Time-based | show monthly revenue trends | ✅ Works |
| Subquery | show most expensive product ordered by each customer | 🔄 Repair loop |
| Window functions | rank customers by spending within each city | 🔄 Repair loop |
| Complex analytics | show month over month revenue growth | ❌ Needs improvement |

✅ Direct — generated and executed correctly on first attempt
🔄 Repair loop — failed initially, automatically repaired and executed
❌ Failed — beyond current model capability, identified as a known limitation

---

## Known Limitations

- **SQL accuracy depends on model quality** — complex window functions and multi-step analytics occasionally require the repair loop or fail entirely. Upgrading to a stronger model improves this significantly.
- **Schema inference is pattern-based** — implicit relationship detection relies on `_id` naming conventions. Databases with non-standard naming may miss some relationships.
- **Single database** — currently configured for one PostgreSQL database. Multi-tenant support with per-user database connections is planned.
- **Memory contamination risk** — only verified successful queries are stored in vector memory. Failed queries are discarded to prevent bad SQL from polluting future retrievals.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI, Python |
| Database | PostgreSQL, SQLAlchemy, psycopg2 |
| AI | Groq, Llama 3.3 70B |
| RAG | sentence-transformers, cosine similarity |
| Frontend | React, Vite, CSS |

---

## Project Structure

```
askbase/
├── backend/
│   ├── main.py                  — FastAPI routes
│   ├── core/
│   │   └── database.py          — DB connection
│   ├── services/
│   │   ├── schema_service.py    — schema extraction
│   │   ├── memory_service.py    — RAG vector memory
│   │   ├── query_service.py     — SQL execution
│   │   └── log_service.py       — query logging
│   └── ai/
│       ├── sql_generator.py     — prompt builder + SQL cleaner
│       └── providers/
│           └── groq_provider.py — Groq LLM integration
└── frontend/
    └── src/
        ├── App.jsx
        ├── SchemaPanel.jsx      — live schema browser
        └── QueryPanel.jsx       — query interface + results
```

---

## Planned Features

- Multi-tenant support — users connect their own databases
- Encrypted credential storage — Fernet encryption for DB URLs
- Embedding-based schema retrieval — semantic table selection for large DBs
- SQL validation layer — column existence checks before execution
- Support for MySQL, SQLite, and other dialects
- Charts and data visualization in the results panel

---

## Local Setup

**Backend**
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

**Frontend**
```bash
cd frontend
npm install
npm run dev
```

**Environment variables** — create a `.env` file in the backend folder:
```
GROQ_API_KEY=your_groq_api_key
DATABASE_URL=postgresql://user:password@localhost:5432/yourdb
```
