from core.database import get_db_connection

def log_query(question, sql_query):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO query_logs (question, generated_sql) VALUES (%s, %s)",
        (question, sql_query)
    )

    conn.commit()
    cur.close()
    conn.close()