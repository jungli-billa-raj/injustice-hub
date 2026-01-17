import sqlite3
from processor.classifier import classify
from llm.ollama import OllamaClient
from llm.validator import validate_case_json
from processor.validator import validate_case
from processor.policy import should_accept_case

# from extractor import extract_case

DB_PATH = "data/injustice.db"


def main():
    # llm = OllamaClient(host="192.168.29.210:11434", model="phi3:medium")
    llm = OllamaClient(host="192.168.29.210:11434", model="qwen2.5:0.5b")
    stats = {
        "total": 0,
        "classified_crime": 0,
        "accepted": 0,
        "inserted": 0,
    }

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # Fetch unprocessed articles (modify limit for testing)
    # cur.execute("""
    #     SELECT *
    #     FROM raw_articles
    #     WHERE id NOT IN (
    #         SELECT source_article_id FROM cases
    #     )
    #     ORDER BY published_at
    #     LIMIT 200
    # """)
    cur.execute("""
    SELECT *
    FROM raw_articles
    WHERE id NOT IN (
        SELECT source_article_id FROM cases
    )
    ORDER BY published_at
    LIMIT 200
    """)

    articles = cur.fetchall()
    print(f"Processing {len(articles)} articles")

    for article in articles:
        stats["total"] += 1

        try:
            is_crime, confidence = classify(article["headline"])
        except Exception as e:
            print(f"\nAn exception occured in classify(): {e}\n")
            print("continuing")
            continue

        if is_crime:
            stats["classified_crime"] += 1

        if not should_accept_case(is_crime, confidence):
            continue

        # count of cases accepted for processing
        stats["accepted"] += 1

        print(f"processing full_text: {article['full_text']}")
        try:
            raw = llm.extract_case(article["full_text"])
        except Exception as e:
            print(f"\nAn exception occured in extract_case(): {e}\n")
            print("continuing")
            continue

        if raw is None:
            continue
        print(f"full text: {raw}")
        try:
            case = validate_case_json(raw)

            if not validate_case(case):
                continue
        except Exception as e:
            print(
                f"\nLLM didnot give proper result. Skipping article: {
                    article['headline']
                }\n"
            )
            print(f"Error: {e}")
            continue

        print("validated")
        print("Inserting into DB\n------------")

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
        if cur.rowcount == 1:
            stats["inserted"] += 1
            conn.commit()

    print("Pipeline stats:")
    for k, v in stats.items():
        print(f"  {k}: {v}")

    conn.close()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
