from core.database import get_db_connection
from sentence_transformers import SentenceTransformer, util
import json
import torch


# Load model once
model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_embedding(text: str):

    embedding = model.encode(text)

    return embedding.tolist()


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

    query_embedding = model.encode(
        question,
        convert_to_tensor=True
    )

    similarities = []

    for q, sql, emb in rows:

        stored_embedding = torch.tensor(
            json.loads(emb),
            dtype=torch.float
        )

        score = util.cos_sim(
            query_embedding,
            stored_embedding
        ).item()

        similarities.append((score, q, sql))

    similarities.sort(
        reverse=True,
        key=lambda x: x[0]
    )

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
        INSERT INTO query_memory
        (question, sql_query, embedding)

        VALUES (%s, %s, %s)
        """,
        (
            question,
            sql_query,
            json.dumps(embedding)
        )
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