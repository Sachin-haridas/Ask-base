from core.database import get_db_connection


def execute_query(sql_query):

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(sql_query)

        # SELECT queries
        if cursor.description:

            rows = cursor.fetchall()

            columns = [desc[0] for desc in cursor.description]

            results = []

            for row in rows:
                results.append(dict(zip(columns, row)))

            return results

        # Non-SELECT queries
        conn.commit()

        return {"message": "Query executed successfully"}

    except Exception as e:

        return {"error": str(e)}

    finally:

        cursor.close()
        conn.close()