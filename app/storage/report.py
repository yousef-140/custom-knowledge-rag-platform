import sqlite3
from pathlib import Path


DB_PATH = Path("data/monitoring.db")


def get_connection():
    return sqlite3.connect(DB_PATH)


def get_total_queries():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM queries")
    count = cur.fetchone()[0]
    conn.close()
    return count


def get_average_latency():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT AVG(latency) FROM queries")
    value = cur.fetchone()[0]
    conn.close()
    return value if value is not None else 0.0


def get_recent_queries(limit=5):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, query, latency, created_at
        FROM queries
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))
    rows = cur.fetchall()
    conn.close()
    return rows


def get_most_frequent_chunks(limit=5):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT chunk_id, COUNT(*) as freq
        FROM retrievals
        GROUP BY chunk_id
        ORDER BY freq DESC
        LIMIT ?
    """, (limit,))
    rows = cur.fetchall()
    conn.close()
    return rows


def print_report():
    total_queries = get_total_queries()
    avg_latency = get_average_latency()
    recent_queries = get_recent_queries()
    frequent_chunks = get_most_frequent_chunks()

    print("=" * 60)
    print("RAG Monitoring Report")
    print("=" * 60)
    print(f"Total queries       : {total_queries}")
    print(f"Average latency     : {avg_latency:.4f} sec")
    print("-" * 60)

    print("Recent Queries:")
    for q in recent_queries:
        print(f"  id={q[0]} | latency={q[2]:.4f} | {q[1]}")

    print("-" * 60)

    print("Most Frequent Retrieved Chunks:")
    for chunk_id, freq in frequent_chunks:
        print(f"  chunk_id={chunk_id} | retrieved {freq} times")

    print("=" * 60)