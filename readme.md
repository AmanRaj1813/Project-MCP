# GNews MCP Server

A Model Context Protocol (MCP) server built using FastMCP and the GNews API to fetch real-time news headlines, search articles, retrieve topic-based news, and filter articles by date range.

---

# Project Overview

This project demonstrates how to:

- Build MCP tools using FastMCP
- Integrate third-party REST APIs
- Use asynchronous Python programming
- Secure API keys using environment variables
- Test MCP tools using MCP Inspector

The server exposes multiple news-related tools powered by the GNews API.

---

# Features

## Implemented MCP Tools

### 1. get_top_headlines
Fetches top headlines by category, country, and language.

Supported categories include:
- technology
- business
- sports
- entertainment
- health
- science

---

### 2. search_news
Searches news articles using keywords or phrases.

Supports:
- keyword filtering
- sorting by:
  - publishedAt
  - relevance

---

### 3. get_news_by_topic
Fetches articles for predefined topics.

Supported topics:
- breaking-news
- world
- nation
- business
- technology
- entertainment
- sports
- science
- health

Includes validation for unsupported topics.

---

### 4. get_news_by_date_range
Custom tool implemented as part of the assignment.

Features:
- search within date ranges
- validates date format
- validates from_date < to_date
- handles empty results gracefully

---

# Technologies Used

- Python 3.10+
- FastMCP
- HTTPX
- python-dotenv
- GNews REST API
- MCP Inspector

---

# Project Structure

```text
gnews_mcp/
├── app/
│   ├── __init__.py
│   └── server.py
├── .env
├── README.md
├── requirements.txt
└── pyproject.toml


# Useful Commands

## Start MCP Inspector

```bash
npx @modelcontextprotocol/inspector python app/server.py
```

## Run with Custom Ports (PowerShell)

```powershell
$env:PORT=8080
$env:CLIENT_PORT=8081
$env:SERVER_PORT=8082

npx @modelcontextprotocol/inspector python app/server.py
```

## Install Dependencies

```bash
pip install "mcp[cli]" httpx python-dotenv
```