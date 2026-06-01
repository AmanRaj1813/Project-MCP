import os
from datetime import datetime
from typing import Optional

import httpx
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# Load environment variables
load_dotenv()

API_KEY = os.getenv("GNEWS_API_KEY")
BASE_URL = "https://gnews.io/api/v4"

# Initialize MCP server
mcp = FastMCP("GNews MCP Server")


def format_articles(articles: list) -> str:
    """
    Format articles into readable text.
    """

    if not articles:
        return "No articles found."

    output = []

    for idx, article in enumerate(articles, start=1):
        output.append(
            f"""
Article {idx}
Title: {article.get("title")}
Source: {article.get("source", {}).get("name")}
Published: {article.get("publishedAt")}
URL: {article.get("url")}
Description: {article.get("description")}
"""
        )

    return "\n".join(output)


async def fetch_news(endpoint: str, params: dict) -> dict:
    """
    Generic helper function to call GNews API.
    """

    if not API_KEY:
        return {"error": "Missing GNEWS_API_KEY in environment variables."}

    params["apikey"] = API_KEY

    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.get(
                f"{BASE_URL}/{endpoint}",
                params=params
            )

            response.raise_for_status()

            return response.json()

    except httpx.HTTPStatusError as e:
        return {"error": f"HTTP Error: {e.response.text}"}

    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
async def get_top_headlines(
    category: str = "general",
    country: str = "in",
    language: str = "en",
    max_results: int = 10
) -> str:
    """
    Fetch top headlines by category and region.
    """

    params = {
        "category": category,
        "country": country,
        "lang": language,
        "max": max_results,
    }

    data = await fetch_news("top-headlines", params)

    if "error" in data:
        return data["error"]

    return format_articles(data.get("articles", []))


@mcp.tool()
async def search_news(
    query: str,
    language: str = "en",
    max_results: int = 10,
    sort_by: str = "publishedAt"
) -> str:
    """
    Search articles by keyword or phrase.
    """

    allowed_sort = ["publishedAt", "relevance"]

    if sort_by not in allowed_sort:
        return (
            f"Invalid sort_by value. "
            f"Allowed values: {allowed_sort}"
        )

    params = {
        "q": query,
        "lang": language,
        "max": max_results,
        "sortby": sort_by,
    }

    data = await fetch_news("search", params)

    if "error" in data:
        return data["error"]

    return format_articles(data.get("articles", []))


@mcp.tool()
async def get_news_by_topic(
    topic: str,
    language: str = "en",
    max_results: int = 10
) -> str:
    """
    Get news articles by topic.
    """

    allowed_topics = [
        "breaking-news",
        "world",
        "nation",
        "business",
        "technology",
        "entertainment",
        "sports",
        "science",
        "health"
    ]

    # Normalize input
    topic = topic.strip().lower()

    if topic not in allowed_topics:
        return (
            f"Unsupported topic: {topic}\n\n"
            f"Allowed topics: {', '.join(allowed_topics)}"
        )

    params = {
        "topic": topic,
        "lang": language,
        "max": max_results,
    }

    data = await fetch_news("top-headlines", params)

    if "error" in data:
        return data["error"]

    return format_articles(data.get("articles", []))

@mcp.tool()
async def get_news_by_date_range(
    query: str,
    from_date: str,
    to_date: str,
    max_results: int = 10
) -> str:
    """
    Search news articles within a date range.
    """

    try:
        from_dt = datetime.strptime(from_date, "%Y-%m-%d")
        to_dt = datetime.strptime(to_date, "%Y-%m-%d")

        if from_dt > to_dt:
            return (
                "Error: from_date must be earlier "
                "than to_date."
            )

    except ValueError:
        return (
            "Invalid date format. "
            "Use YYYY-MM-DD."
        )

    params = {
        "q": query,
        "from": from_date,
        "to": to_date,
        "max": max_results,
    }

    data = await fetch_news("search", params)

    if "error" in data:
        return data["error"]

    return format_articles(data.get("articles", []))


if __name__ == "__main__":
    mcp.run()