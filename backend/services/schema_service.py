from core.database import get_db_connection


def get_schema():
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    SELECT table_name, column_name
    FROM information_schema.columns
    WHERE table_schema = 'public'
    ORDER BY table_name;
    """

    cursor.execute(query)
    rows = cursor.fetchall()

    schema = {}

    for table, column in rows:
        if table not in schema:
            schema[table] = []

        schema[table].append(column)

    cursor.close()
    conn.close()

    return schema