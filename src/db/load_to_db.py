import sqlite3
import pandas as pd
import os

# Paths
CSV_PATH = "data/processed/manufacturing_clean.csv"
DB_PATH = "src/db/manufacturing.db"

def load_to_database():
    # Load cleaned CSV
    df = pd.read_csv(CSV_PATH)

    # Connect to SQLite (creates DB file if missing)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Create table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS manufacturing (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            year INTEGER,
            month INTEGER,
            value REAL,
            date TEXT
        )
    """)

    # Insert data
    df["date"] = df["year"].astype(str) + "-" + df["month"].astype(str) + "-01"

    df.to_sql("manufacturing", conn, if_exists="replace", index=False)

    conn.commit()
    conn.close()

    print(f"Loaded data into SQLite database at: {DB_PATH}")


if __name__ == "__main__":
    load_to_database()
