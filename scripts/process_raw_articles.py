import sqlite3
import os

from llm.local import LocalLLMClient
from llm.validator import validate_case_json
from llm.exceptions import InvalidLLMResponse


# -------------------------
# Configuration
# -------------------------

# Number of articles to process per run (MVP-safe)
BATCH_SIZE = 5


def get_db_connection():
    """
    Returns a SQLite connection to the project database
    using an absolute path (safe & predictable).
    """
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    db_path = os.path.join(base_dir, "data", "injustice.db")
    return sqlite3.connect(db_path)


def fetch_unprocessed_articles(conn, limit):
    """
    Fetch raw articles that do NOT yet have a case entry.

    This prevents duplicate processing.
    """
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, full_text
        FROM raw_articles
        WHERE id NOT IN (
            SELECT source_article_id FROM cases
        )
        LIMIT ?
        """,
        (limit,),
    )

    return cursor.fetchall()


def insert_case(conn, source_article_id, case_data):
    """
    Insert a validated case into the cases table.
    """
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO cases (
            source_article_id,
            blamed_entity,
            entity_type,
            location,
            crime_description,
            severity,
            blame_status,
            justice_status,
            confidence_score
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            source_article_id,
            case_data["blamed_entity"],
            case_data["entity_type"],
            case_data["location"],
            case_data["crime_description"],
            case_data["severity"],
            case_data["blame_status"],
            case_data["justice_status"],
            case_data["confidence_score"],
        ),
    )

    conn.commit()


def main():
    """
    Main processing loop:
    - Fetch raw articles
    - Extract structured data via LLM
    - Validate output
    - Store results
    """

    conn = get_db_connection()
    llm = LocalLLMClient()

    articles = fetch_unprocessed_articles(conn, BATCH_SIZE)

    if not articles:
        print("No unprocessed articles found.")
        return

    for article_id, article_text in articles:
        try:
            # 1️⃣ Call LLM
            raw_case = llm.extract_case(article_text)

            # 2️⃣ Validate LLM output
            validated_case = validate_case_json(raw_case)

            # 3️⃣ Insert into DB
            insert_case(conn, article_id, validated_case)

            print(f"Processed article ID {article_id}")

        except InvalidLLMResponse as e:
            # LLM returned garbage → skip safely
            print(f"Validation failed for article {article_id}: {e}")

        except Exception as e:
            # Any unexpected failure → log & continue
            print(f"Unexpected error for article {article_id}: {e}")

    conn.close()


if __name__ == "__main__":
    main()
