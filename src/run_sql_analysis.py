import os
import sqlite3
import pandas as pd


# --------------------------------------------------
# Paths
# --------------------------------------------------

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

DATABASE_PATH = os.path.join(
    BASE_DIR,
    "data",
    "amazon_reviews.db"
)

SQL_PATH = os.path.join(
    BASE_DIR,
    "sql",
    "analysis.sql"
)


# --------------------------------------------------
# Execute SQL Analysis
# --------------------------------------------------

def run_analysis():

    print("=" * 70)
    print("AMAZON REVIEWS - SQL ANALYSIS")
    print("=" * 70)

    connection = sqlite3.connect(DATABASE_PATH)

    try:

        with open(SQL_PATH, "r", encoding="utf-8") as file:
            sql_script = file.read()

        # Split the SQL file into individual queries
        queries = [
            query.strip()
            for query in sql_script.split(";")
            if query.strip()
        ]

        for number, query in enumerate(queries, start=1):

            print("\n" + "=" * 70)
            print(f"QUERY {number}")
            print("=" * 70)

            result = pd.read_sql_query(
                query,
                connection
            )

            print(result.to_string(index=False))

    finally:
        connection.close()


# --------------------------------------------------
# Main
# --------------------------------------------------

if __name__ == "__main__":
    run_analysis()