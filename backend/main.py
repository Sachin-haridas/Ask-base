from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import time

from core.database import get_db_connection

from services.query_service import execute_query
from services.schema_service import get_schema
from services.log_service import log_query

from services.memory_service import (
    store_query_memory,
    get_past_queries,
    get_similar_queries
)

from ai.sql_generator import (
    generate_sql,
    repair_sql
)

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173",
                  "https://ask-base-five.vercel.app"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class QuestionRequest(BaseModel):
    question: str


class RunQueryRequest(BaseModel):
    query: str


@app.post("/ask")
def ask_question(data: QuestionRequest):
    try:
        question = data.question

        print("ENDPOINT HIT", flush=True)
        print("Question:", question, flush=True)

        past_queries = get_past_queries()

        print("MEMORY:", past_queries)

        similar_queries = get_similar_queries(question)

        print("SIMILAR:", similar_queries)

        sql_query = generate_sql(
            question,
            similar_queries
        )

        sql_query = sql_query.strip().rstrip(";")

        dangerous = [
            "drop",
            "delete",
            "truncate",
            "alter",
            "update"
        ]

        if any(word in sql_query.lower() for word in dangerous):

            raise HTTPException(
                status_code=400,
                detail="Unsafe SQL query blocked"
            )

        if "limit" not in sql_query.lower():
            sql_query += " LIMIT 100"

        log_query(question, sql_query)

        start = time.time()

        result = execute_query(sql_query)

        # Auto repair
        max_retries = 2
        attempt = 0

        while (
            isinstance(result, dict)
            and "error" in result
            and attempt < max_retries
        ):

            print("SQL ERROR:", result["error"])

            schema = get_schema()

            fixed_sql = repair_sql(
                sql_query,
                result["error"],
                schema
            )

            print("REPAIRED SQL:", fixed_sql)

            result = execute_query(fixed_sql)

            sql_query = fixed_sql

            attempt += 1

        # Store only successful queries
        if not (
            isinstance(result, dict)
            and "error" in result
        ):

            store_query_memory(
                question,
                sql_query
            )

            print("STORED IN MEMORY ✅")

        else:

            print("NOT STORED ❌")

        execution_time = time.time() - start

        return {
            "generated_sql": sql_query,
            "execution_time": execution_time,
            "result": result
        }
        
    except Exception as e:
        import traceback
        error_msg = f"{str(e)}\n{traceback.format_exc()}"
        print("ERROR IN /ask:", error_msg, flush=True)
        raise HTTPException(status_code=500, detail=error_msg)


@app.post("/run-query")
def run_query(data: RunQueryRequest):

    result = execute_query(data.query)

    return {"result": result}


@app.get("/schema")
def schema():

    result = get_schema()

    return {"schema": result}


@app.get("/")
def root():

    return {
        "message": "AI Data Analyst Backend Running"
    }


@app.get("/test-db")
def test_db():

    conn = get_db_connection()

    if conn:

        try:

            cur = conn.cursor()

            cur.execute("SELECT version();")

            result = cur.fetchone()

            cur.close()
            conn.close()

            return {
                "status": "success",
                "message": "Database connection successful",
                "result": result
            }

        except Exception as e:

            raise HTTPException(
                status_code=500,
                detail=f"Database query error: {str(e)}"
            )

    else:

        raise HTTPException(
            status_code=500,
            detail="Failed to connect to database."
        )