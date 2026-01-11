import sqlite3
from classifier import classify
from llm.local import LocalLLMClient
from llm.validtaor import validate_case_json
from llm.exceptions import LLMValidationError
from validtaor import validate_case
from policy import should_accept_case

# from extractor import extract_case

DB_PATH = "data/injustice.db"


def main():
    llm = LocalLLMClient()
    stats = {
        "total": 0,
        "classified_crime": 0,
        "accepted": 0,
        "inserted": 0,
    }

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # Fetch unprocessed articles
    cur.execute("""
        SELECT *
        FROM raw_articles
        WHERE id NOT IN (
            SELECT source_article_id FROM cases
        )
        ORDER BY published_at
        LIMIT 50
    """)

    articles = cur.fetchall()
    print(f"Processing {len(articles)} articles")

    for article in articles:
        stats["total"] += 1
        is_crime, confidence = classify(article["headline"])

        if is_crime:
            stats["classified_crime"] += 1

        if not should_accept_case(is_crime, confidence):
            continue

        stats["accepted"] += 1

        try:
            raw = llm.extract_case(article["full_text"])
            case = validate_case_json(raw)
        except LLMValidationError:
            continue

        if not validate_case(case):
            continue

        cur.execute(
            """
            INSERT OR IGNORE INTO cases (
                source_article_id,
                blamed_entity,
                entity_type,
                location,
                crime_description,
                severity,
                blame_status,
                justice_status,
                confidence_score
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                article["id"],
                case["blamed_entity"],
                case["entity_type"],
                case["location"],
                case["crime_description"],
                case["severity"],
                case["blame_status"],
                case["justice_status"],
                confidence,
            ),
        )

        stats["inserted"] += 1

    conn.commit()

    print("Pipeline stats:")
    for k, v in stats.items():
        print(f"  {k}: {v}")

    conn.close()


if __name__ == "__main__":
    main()
