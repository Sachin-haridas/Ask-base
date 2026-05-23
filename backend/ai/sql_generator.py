from services.schema_service import get_schema
from ai.providers.groq_provider import generate_sql_groq

SQL_KEYWORDS = (
    "select",
    "with",
    "insert",
    "update",
    "delete"
)

def clean_sql(response_text):

    lines = response_text.strip().split("\n")

    for i, line in enumerate(lines):
        cleaned = line.strip()
        if cleaned.lower().startswith(SQL_KEYWORDS):
            # return from this line to the END — not just this line
            return "\n".join(lines[i:]).strip()

    return response_text.strip()
    
def generate_sql(question, similar_queries=None):


    from services.schema_context_service import build_llm_schema_context

    schema_text = build_llm_schema_context()

 

    # 🔥 Add memory (similar queries)
    memory_text = ""
    if similar_queries:
        for q, sql in similar_queries:
            memory_text += f"Q: {q}\nSQL: {sql}\n\n"

    prompt = f"""
You are a PostgreSQL SQL generator.

Database schema:
{schema_text}

Relevant past queries:
{memory_text}

Rules:
- Always include a FROM clause
- Use EXACT table and column names from schema (no guessing)
- Do NOT change singular/plural forms
- Return ONLY SQL
- No explanation
- No markdown
- Add LIMIT 100 unless it is an aggregate query

User request:
{question}

SQL:
"""

    raw_sql = generate_sql_groq(prompt)

    return clean_sql(raw_sql)


def repair_sql(bad_sql, error_message, schema):

    # convert schema dict → readable text
    schema_text = ""
    for table, columns in schema.items():
        schema_text += f"Table: {table}\nColumns: {', '.join(columns)}\n\n"

    prompt = f"""
You are a PostgreSQL expert.

The following SQL query caused an error.

Database schema:
{schema_text}

SQL query:
{bad_sql}

Database error:
{error_message}

Fix the SQL so it runs correctly.

Rules:
- Return ONLY raw SQL
- Do NOT explain anything
- Do NOT include English sentences
- Do NOT include markdown
- Output must start directly with SQL keyword   
"""

    fixed_sql = generate_sql_groq(prompt)

    # clean markdown + extra text
    fixed_sql = generate_sql_groq(prompt)
    fixed_sql = clean_sql(fixed_sql)

    return fixed_sql