import os
import sqlite3
import pandas as pd


# --------------------------------------------------
# Paths
# --------------------------------------------------

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

RAW_DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "raw",
    "Reviews.csv"
)

DATABASE_PATH = os.path.join(
    BASE_DIR,
    "data",
    "amazon_reviews.db"
)

SCHEMA_PATH = os.path.join(
    BASE_DIR,
    "sql",
    "schema.sql"
)


# --------------------------------------------------
# Load Schema
# --------------------------------------------------

def create_database(connection):
    """
    Create the reviews table using schema.sql.
    """

    with open(SCHEMA_PATH, "r", encoding="utf-8") as file:
        schema = file.read()

    connection.executescript(schema)


# --------------------------------------------------
# Load CSV into SQLite
# --------------------------------------------------

def load_data():

    print("Loading dataset...")

    df = pd.read_csv(RAW_DATA_PATH)

    print(f"Rows loaded: {len(df):,}")

    # Rename columns to match our SQL schema
    df = df.rename(columns={
        "Id": "id",
        "ProductId": "product_id",
        "UserId": "user_id",
        "ProfileName": "profile_name",
        "HelpfulnessNumerator": "helpfulness_numerator",
        "HelpfulnessDenominator": "helpfulness_denominator",
        "Score": "score",
        "Time": "review_time",
        "Summary": "summary",
        "Text": "review_text"
    })

    connection = sqlite3.connect(DATABASE_PATH)

    try:

        print("Creating database schema...")

        create_database(connection)

        print("Writing data to SQLite...")

        df.to_sql(
            "reviews",
            connection,
            if_exists="append",
            index=False,
            chunksize=10000
        )

        connection.commit()

        print("\nDatabase created successfully.")
        print(f"Database: {DATABASE_PATH}")

    finally:

        connection.close()


# --------------------------------------------------
# Main
# --------------------------------------------------

if __name__ == "__main__":
    load_data()