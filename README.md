# Ask-base
Askbase — Natural Language Analytics Engine

Askbase lets you query any PostgreSQL database using plain English. 
No SQL knowledge required. Just ask a question and get results instantly.

Built as an AI systems engineering project, Askbase goes far beyond 
a simple LLM wrapper. It combines dynamic schema intelligence, 
vector memory, and automatic error recovery into a full analytics pipeline.

How It Works

You type a question like "show top 5 customers by total spending".
Askbase extracts your database schema automatically, infers relationships 
between tables using foreign keys and naming patterns, retrieves similar 
past queries from vector memory, builds a schema-aware prompt, sends it 
to a Groq-hosted LLM, executes the generated SQL against your PostgreSQL 
database, and returns structured results — all in seconds.

Key Features

Natural Language to SQL — converts plain English questions into 
executable PostgreSQL queries using Groq LLMs with schema-grounded prompting.

Dynamic Schema Extraction — automatically inspects any connected database, 
extracts tables, columns, data types, primary keys, and foreign keys without 
any manual configuration.

ER Relationship Inference — builds entity relationships from both explicit 
foreign keys and inferred naming patterns, helping the AI understand 
how to join tables correctly.

RAG Query Memory — stores successful question and SQL pairs as vector 
embeddings using sentence-transformers. Retrieves semantically similar 
past queries and injects them into the prompt, making the system smarter 
over time.

Automatic SQL Repair Loop — if a query fails, the error message is sent 
back to the LLM which attempts to fix the SQL automatically, retrying 
up to 2 times before giving up.

Security — blocks dangerous queries containing DROP, DELETE, TRUNCATE, 
ALTER, and UPDATE before execution.

Tech Stack

Backend — FastAPI, PostgreSQL, SQLAlchemy, psycopg2
AI — Groq, Llama 3.3 70B, prompt engineering
RAG — sentence-transformers, cosine similarity, vector memory
Frontend — React, Vite, CSS

This project is actively being developed. 
Planned features include multi-tenant support, 
encrypted credential storage, and embedding-based schema retrieval.
