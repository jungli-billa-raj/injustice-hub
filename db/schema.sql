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

