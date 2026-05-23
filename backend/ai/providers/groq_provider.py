import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SQL_KEYWORDS = ("select", "with", "insert", "update", "delete")

def generate_sql_groq(prompt):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are a SQL expert. Return only valid SQL queries, no explanation."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0,
        max_tokens=500,  # increased — 200 was cutting off long queries
        top_p=0.1,
    )

    result = response.choices[0].message.content
    print("\nRAW GROQ OUTPUT:\n", result)

    # remove markdown
    result = result.replace("```sql", "").replace("```", "").strip()

    # find where SQL starts, return everything from there
    lines = result.split("\n")
    for i, line in enumerate(lines):
        if line.strip().lower().startswith(SQL_KEYWORDS):
            return "\n".join(lines[i:]).strip()

    return result.strip()