import sqlite3
from pathlib import Path

DB_PATH = Path("data/monitoring.db")

def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    connect = get_connection()
    cur = connect.cursor()


    cur.execute("""
    CREATE TABLE IF NOT EXISTS queries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        query TEXT,
        answer TEXT,
        latency REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS retrievals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        query_id INTEGER,
        chunk_id TEXT,
        score REAL,
        rank INTEGER
    )
    """)


    connect.commit()

    connect.close()

def log_query(query, answer, latency):
    connect = get_connection()
    cur = connect.cursor()

    cur.execute(
        "INSERT INTO queries(query, answer, latency) VALUES (?, ?, ?)",
        (query, answer, latency)
    )

    query_id = cur.lastrowid

    connect.commit()
    connect.close()

    return query_id


def log_retrieval(query_id,results):
    connect = get_connection()

    cur = connect.cursor()

    for rank, r in enumerate(results, start=1):
        cur.execute(
            """
            INSERT INTO retrievals(query_id, chunk_id, score, rank)
            VALUES (?, ?, ?, ?)
            """,
            (
                query_id,
                r["chunk_id"],
                r.get("hybrid_score", r.get("score")),
                rank
            )
        )

    connect.commit()
    connect.close()