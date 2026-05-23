from core.database import get_db_connection
import json
import math
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# ─────────────────────────────────────────────
# EMBEDDING — uses Groq API instead of local model
# No torch, no sentence-transformers, no RAM issues
# ─────────────────────────────────────────────

def generate_embedding(text: str) -> list:
    response = genai.embeddings.create(
        model="models/text-embedding-004",
        input=text
    )
    return response["embedding"]


# ─────────────────────────────────────────────
# COSINE SIMILARITY — pure python, no torch needed
# ─────────────────────────────────────────────

def cosine_similarity(vec_a, vec_b):
    dot = sum(a * b for a, b in zip(vec_a, vec_b))
    mag_a = math.sqrt(sum(a * a for a in vec_a))
    mag_b = math.sqrt(sum(b * b for b in vec_b))
    if mag_a == 0 or mag_b == 0:
        return 0.0
    return dot / (mag_a * mag_b)


def get_similar_queries(question, top_k=3):

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT question, sql_query, embedding FROM query_memory"
    )

    rows = cur.fetchall()
    cur.close()
    conn.close()

    if not rows:
        return []

    query_embedding = generate_embedding(question)

    similarities = []

    for q, sql, emb in rows:
        stored_embedding = json.loads(emb)
        score = cosine_similarity(query_embedding, stored_embedding)
        similarities.append((score, q, sql))

    similarities.sort(reverse=True, key=lambda x: x[0])

    return [
        (q, sql)
        for _, q, sql in similarities[:top_k]
    ]


def store_query_memory(question, sql_query):

    conn = get_db_connection()
    cur = conn.cursor()

    embedding = generate_embedding(question)

    cur.execute(
        """
        INSERT INTO query_memory (question, sql_query, embedding)
        VALUES (%s, %s, %s)
        """,
        (question, sql_query, json.dumps(embedding))
    )

    conn.commit()
    cur.close()
    conn.close()


def get_past_queries(limit=5):

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT question, sql_query
        FROM query_memory
        ORDER BY created_at DESC
        LIMIT %s
        """,
        (limit,)
    )

    rows = cur.fetchall()
    cur.close()
    conn.close()

    return rows