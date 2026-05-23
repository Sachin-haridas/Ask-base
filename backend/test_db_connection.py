from core.database import get_db_connection

if __name__ == "__main__":
    conn = get_db_connection()
    if conn:
        print("Connection successful!")
        conn.close()
    else:
        print("Connection failed.")
