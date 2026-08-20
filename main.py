import requests

USERNAME = "USERNAME"
PASSWORD = "PASSWORD"

API_URL = "https://realtime.oxylabs.io/v1/queries"


def scrape_google_scholar(query, start_page=1, pages=1, geo_location=None):
    """Scrape Google Scholar via the dedicated `google_scholar` source."""
    payload = {
        "source": "google_scholar",
        "query": query,
        "start_page": start_page,
        "pages": pages,
        "parse": True,
    }
    if geo_location:
        payload["geo_location"] = geo_location

    response = requests.post(
        API_URL,
        auth=(USERNAME, PASSWORD),
        json=payload,
        timeout=180,
    )
    response.raise_for_status()
    return response.json()["results"]


def extract_articles(results):
    """Flatten parsed results into a simple list of articles."""
    articles = []
    for result in results:
        content = result["content"]
        for item in content.get("organic", []):
            publication_info = item.get("publication_info", {})
            inline_links = item.get("inline_links", {})
            cited_by = inline_links.get("cited_by", {})

            articles.append(
                {
                    "position": item.get("pos"),
                    "title": item.get("title"),
                    "url": item.get("url"),
                    "result_type": item.get("result_type"),
                    "description": item.get("description"),
                    "authors": [
                        author["name"]
                        for author in publication_info.get("authors", [])
                    ],
                    "publication_summary": publication_info.get("summary"),
                    "cited_by_count": cited_by.get("total", 0),
                    "cited_by_url": cited_by.get("url"),
                    "cite_url": inline_links.get("cite_url"),
                    "pdf_links": [
                        resource["url"]
                        for resource in item.get("resources", [])
                        if resource.get("file_format") == "PDF"
                    ],
                }
            )
    return articles


if __name__ == "__main__":
    results = scrape_google_scholar("global warming", start_page=1, pages=2)
    articles = extract_articles(results)

    for article in articles:
        print(f"{article['position']}. {article['title']}")
        print(f"   Authors: {', '.join(article['authors']) or 'n/a'}")
        print(f"   Cited by: {article['cited_by_count']}")
        print(f"   URL: {article['url']}")
        if article["pdf_links"]:
            print(f"   PDF: {article['pdf_links'][0]}")
        print()
