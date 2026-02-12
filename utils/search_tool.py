import requests
import os
from dotenv import load_dotenv

load_dotenv()

SERPAPI_KEY = os.getenv("SERPAPI_KEY")

def search_web(query: str):
    url = "https://serpapi.com/search"

    params = {
        "q": query,
        "api_key": SERPAPI_KEY,
        "engine": "google",
        "num": 5
    }

    response = requests.get(url, params=params)
    data = response.json()

    if "error" in data:
        return "Error fetching live data."

    results = data.get("organic_results", [])

    if not results:
        return "No live data found."

    summary = ""

    for result in results[:5]:
        title = result.get("title", "")
        snippet = result.get("snippet", "")
        link = result.get("link", "")

        summary += f"Title: {title}\nSnippet: {snippet}\nSource: {link}\n\n"

    return summary
