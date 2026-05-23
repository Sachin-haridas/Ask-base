# from core.database import DATABASE_URL
from sqlalchemy import create_engine, inspect
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
inspector = inspect(engine)

# rest of your code stays exactly the same

engine = create_engine(DATABASE_URL)
inspector = inspect(engine)


def extract_schema_and_relationships():

    tables = inspector.get_table_names()

    schema = {}
    relationships = []

    # ----------------------------
    # EXTRACT TABLES + COLUMNS
    # ----------------------------
    for table in tables:

        columns_info = inspector.get_columns(table)

        columns = []

        for col in columns_info:
            columns.append(col["name"])

        schema[table] = columns

    # ----------------------------
    # EXTRACT EXPLICIT FOREIGN KEYS
    # ----------------------------
    for table in tables:

        foreign_keys = inspector.get_foreign_keys(table)

        for fk in foreign_keys:

            source_columns = fk["constrained_columns"]
            target_table = fk["referred_table"]
            target_columns = fk["referred_columns"]

            relationships.append({
                "source_table": table,
                "source_columns": source_columns,
                "target_table": target_table,
                "target_columns": target_columns,
                "type": "explicit"
            })

    # ----------------------------
    # INFER IMPLICIT RELATIONSHIPS
    # ----------------------------
    for table_a in tables:

        columns_a = schema[table_a]

        for table_b in tables:

            if table_a == table_b:
                continue

            columns_b = schema[table_b]

            for col_a in columns_a:

                if col_a.endswith("_id"):

                    if col_a in columns_b:

                        # avoid duplicates
                        already_exists = any(
                            r["source_table"] == table_a
                            and r["target_table"] == table_b
                            and col_a in r["source_columns"]
                            for r in relationships
                        )

                        if not already_exists:

                            relationships.append({
                                "source_table": table_a,
                                "source_columns": [col_a],
                                "target_table": table_b,
                                "target_columns": [col_a],
                                "type": "inferred"
                            })

    return {
        "schema": schema,
        "relationships": relationships
    }


def build_llm_schema_context():

    data = extract_schema_and_relationships()

    schema = data["schema"]
    relationships = data["relationships"]

    context = ""

    # ----------------------------
    # TABLES + COLUMNS
    # ----------------------------
    context += "DATABASE SCHEMA:\n\n"

    for table, columns in schema.items():

        context += f"Table: {table}\n"
        context += f"Columns: {', '.join(columns)}\n\n"

    # ----------------------------
    # RELATIONSHIPS
    # ----------------------------
    context += "\nDATABASE RELATIONSHIPS:\n\n"

    for rel in relationships:

        source = rel["source_table"]
        source_cols = ", ".join(rel["source_columns"])

        target = rel["target_table"]
        target_cols = ", ".join(rel["target_columns"])

        rel_type = rel["type"]

        context += (
            f"{source}.{source_cols} "
            f"→ "
            f"{target}.{target_cols} "
            f"({rel_type})\n"
        )

    return context  