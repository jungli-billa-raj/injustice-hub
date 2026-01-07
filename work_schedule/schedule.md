# 🚀 Injustice Hub — 5 Day MVP Build Plan

> **Goal:** Ship a minimal, working product that scrapes, structures, stores, and visualizes injustice-related cases between date ranges.

---

## 🟢 Day 1 — Foundation & Data Ingestion

### Objectives

* Set up the project skeleton
* Start collecting raw data

### Tasks

* [ ] Initialize Git repository
* [ ] Create basic folder structure

  ```
  scraper/
  backend/
  llm/
  db/
  frontend/
  ```
* [ ] Design SQLite schema (initial)
* [ ] Set up Scrapy project
* [ ] Write **1 spider** for a single news source
* [ ] Store raw articles in SQLite

### Deliverable

✅ `raw_articles` table populated with real news data

---

## 🟡 Day 2 — Intelligence Layer (LLM Core)

### Objectives

* Convert raw articles into structured injustice data

### Tasks

* [ ] Design **LLM abstraction interface**
* [ ] Implement `LocalLLMClient`
* [ ] Write extraction prompt (JSON-only output)
* [ ] Parse & validate LLM responses
* [ ] Insert structured cases into DB
* [ ] Add confidence score per extraction

### Deliverable

✅ One article → one structured injustice case in DB

---

## 🟠 Day 3 — Backend API (FastAPI)

### Objectives

* Expose stored data via clean APIs

### Tasks

* [ ] Initialize FastAPI app
* [ ] Implement `/cases` endpoint
* [ ] Support `start_date` / `end_date` filters
* [ ] Implement basic stats endpoints:

  * `/stats/severity`
  * `/stats/location`
* [ ] Add CORS support
* [ ] Manual testing via curl / browser

### Deliverable

✅ Backend serving real data over HTTP

---

## 🔵 Day 4 — Frontend (Visualization)

### Objectives

* Make the data visible and explorable

### Tasks

* [ ] Basic HTML layout
* [ ] Fetch data from FastAPI
* [ ] Render table of cases
* [ ] Add date range selector
* [ ] Integrate charts:

  * Severity distribution
  * Location-based counts
* [ ] Add disclaimer text

### Deliverable

✅ Usable UI showing injustice data & trends

---

## 🔴 Day 5 — Cleanup, Dedup & Ship

### Objectives

* Stabilize MVP and prepare for sharing

### Tasks

* [ ] Basic deduplication logic
* [ ] Handle missing / low-confidence cases
* [ ] Improve error handling
* [ ] Write README (purpose, limits, ethics)
* [ ] Add screenshots / demo GIF
* [ ] Final end-to-end test

### Deliverable

🚀 **MVP shipped and demo-ready**

---

## 📌 MVP Success Criteria

* Scrapes real news articles
* Extracts structured injustice data
* Stores and queries historical data
* Displays insights visually
* Clearly communicates limitations
