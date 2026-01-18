from fastapi import FastAPI, Query
from pathlib import Path
import sqlite3
from typing import Dict, Any

app = FastAPI(title="Injustice Hub API")

# --- DB PATH ---
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "injustice.db"

PAGE_SIZE = 10


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def paginate(table: str, page: int, order_by: str = "id") -> Dict[str, Any]:
    offset = (page - 1) * PAGE_SIZE

    conn = get_db_connection()
    cur = conn.cursor()

    # total count
    cur.execute(f"SELECT COUNT(*) FROM {table}")
    total = cur.fetchone()[0]

    # page data
    cur.execute(
        f"""
        SELECT *
        FROM {table}
        ORDER BY {order_by}
        LIMIT ? OFFSET ?
        """,
        (PAGE_SIZE, offset),
    )

    rows = [dict(row) for row in cur.fetchall()]
    conn.close()

    return {
        "page": page,
        "page_size": PAGE_SIZE,
        "total": total,
        "items": rows,
    }


@app.get("/api/raw-articles")
def get_raw_articles(page: int = Query(1, ge=1)):
    return paginate(table="raw_articles", page=page, order_by="published_at")


# @app.get("/api/cases")
# def get_cases(page: int = Query(1, ge=1)):
#     return paginate(table="cases", page=page, order_by="id")
#


@app.get("/api/cases")
def get_cases(page: int = Query(1, ge=1)):
    offset = (page - 1) * PAGE_SIZE

    conn = get_db_connection()
    cur = conn.cursor()

    # total count
    cur.execute("SELECT COUNT(*) FROM cases")
    total = cur.fetchone()[0]

    # joined data
    cur.execute(
        """
        SELECT
            c.*,
            r.url AS article_url
        FROM cases c
        LEFT JOIN raw_articles r
            ON r.id = c.source_article_id
        ORDER BY c.id
        LIMIT ? OFFSET ?
        """,
        (PAGE_SIZE, offset),
    )

    rows = [dict(row) for row in cur.fetchall()]
    conn.close()

    return {
        "page": page,
        "page_size": PAGE_SIZE,
        "total": total,
        "items": rows,
    }
