-- ================================
-- Injustice Hub - Day 1 Schema
-- Purpose: Store RAW scraped news articles
-- NO intelligence, NO interpretation
-- ================================

-- Drop table if it already exists (safe for development)
DROP TABLE IF EXISTS raw_articles;

-- Table to store raw news articles exactly as scraped
CREATE TABLE raw_articles (
    -- Auto-incrementing primary key
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    -- Name of the news source (e.g., "The Hindu", "Indian Express")
    source TEXT NOT NULL,

    -- Original article URL (used for deduplication later)
    url TEXT NOT NULL UNIQUE,

    -- Headline of the article
    headline TEXT NOT NULL,

    -- Published date as provided by the source
    -- Stored as TEXT for flexibility (YYYY-MM-DD preferred)
    published_at TEXT,

    -- Full cleaned article text
    full_text TEXT NOT NULL,

    -- Timestamp when our scraper stored this article
    scraped_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- Index for faster date-based queries later
CREATE INDEX idx_raw_articles_published_at
ON raw_articles (published_at);

-- ================================
-- Derived intelligence table
-- ================================

DROP TABLE IF EXISTS cases;

CREATE TABLE cases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    -- Link back to raw article
    source_article_id INTEGER NOT NULL,

    -- Who is blamed
    blamed_entity TEXT NOT NULL,

    -- Individual or organization (restricted)
    entity_type TEXT NOT NULL
        CHECK (entity_type IN ('individual', 'organization')),

    -- Location string (city/state/country as extracted)
    location TEXT,

    -- Short description of the crime
    crime_description TEXT NOT NULL,

    -- Severity scale (1–10 only)
    severity INTEGER NOT NULL
        CHECK (severity BETWEEN 1 AND 10),

    -- Legal status of blame (restricted)
    blame_status TEXT NOT NULL
        CHECK (blame_status IN ('accused', 'guilty', 'liable')),

    -- Justice outcome (restricted)
    justice_status TEXT NOT NULL
        CHECK (justice_status IN ('served', 'pending', 'escaped')),

    -- How confident the LLM is (0.0–1.0)
    confidence_score REAL NOT NULL
        CHECK (confidence_score BETWEEN 0.0 AND 1.0),

    created_at TEXT NOT NULL DEFAULT (datetime('now')),

    -- Ensure linkage to raw articles
    FOREIGN KEY (source_article_id)
        REFERENCES raw_articles(id)
        ON DELETE CASCADE
);

-- Index for article → case lookup
CREATE INDEX idx_cases_source_article
ON cases (source_article_id);

