# How to Scrape Google Scholar

[![Oxylabs promo code](https://raw.githubusercontent.com/oxylabs/how-to-scrape-google-scholar/refs/heads/main/Google-Scraper-API-1090x275.png)](https://oxylabs.io/products/scraper-api/serp/google?utm_source=877&utm_medium=affiliate&groupid=877&utm_content=how-to-scrape-google-scholar-github&transaction_id=102c8d36f7f0d0e5797b8f26152160)

[![](https://dcbadge.limes.pink/api/server/Pds3gBmKMH?style=for-the-badge&theme=discord)](https://discord.gg/Pds3gBmKMH) [![YouTube](https://img.shields.io/badge/YouTube-Oxylabs-red?style=for-the-badge&logo=youtube&logoColor=white)](https://www.youtube.com/@oxylabs)

[Google Scholar](https://scholar.google.com/) is now a **dedicated source with a dedicated parser** in Oxylabs [Web Scraper API](https://oxylabs.io/products/scraper-api/web). Set `source` to `google_scholar` and `parse` to `true`, and you'll get structured JSON with articles, authors, citation counts, publication info, related searches, and direct links to available PDF documents – no HTML parsing required.

You can get a **1-week free trial** by registering on the [dashboard](https://dashboard.oxylabs.io/).

For a detailed walkthrough with explanations and visuals, check our [blog post](https://oxylabs.io/blog/how-to-scrape-google-scholar). Also, do not hesitate to check this [Best SERP APIs](https://medium.com/@oxylabs.io/the-10-best-serp-apis-in-2025-22bf7f91f8f0) list.

## What's new

Previously, Google Scholar data had to be retrieved through the `google` source together with a `url` parameter, and structured output required building your own [Custom Parser](https://developers.oxylabs.io/products/web-scraper-api/features/custom-parser) instructions.

| | Before | Now |
|---|---|---|
| Source | `google` | `google_scholar` |
| Target selection | `url` with a full `scholar.google.com` link | `query` with a plain search term |
| Structured output | Custom Parser instructions | `"parse": true` |
| Dependencies | `requests` + `beautifulsoup4` | `requests` |

## Requirements

Python 3.8+ and the `requests` library:

```bash
pip install requests
```

## Payload

```json
{
    "source": "google_scholar",
    "query": "global warming",
    "start_page": 1,
    "pages": 2,
    "parse": true
}
```

| Parameter | Description | Default |
|---|---|---|
| `source` | Set to `google_scholar` | – |
| `query` | Search term (UTF-8 encoded) | – |
| `start_page` | Page number to start from | `1` |
| `pages` | Number of pages to retrieve | `1` |
| `parse` | Return structured JSON instead of HTML | `false` |
| `geo_location` | Geographical location to base the search on | – |
| `render` | Set to `html` to enable JavaScript rendering | – |
| `callback_url` | URL to which the result is sent | – |

> **Note:** The `domain` parameter is no longer available for Google sources. Use `geo_location` to localize your searches.

## The complete code

```python
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
```

Replace `USERNAME` and `PASSWORD` with your Web Scraper API credentials and run:

```bash
python main.py
```

## Sample output

Each result in `results` contains a `content` object with `organic`, `pagination`, `related_searches`, and `search_information` keys. A single organic entry looks like this:

```json
{
    "pos": 5,
    "title": "Success with style: Using writing style to predict the success of novels",
    "url": "https://aclanthology.org/D13-1181.pdf",
    "result_type": "pdf",
    "description": "… Predicting success of novels and movies: To the best of our knowledge, our work is the first that provides quantitative insights into the unstudied connection between the writing style …",
    "result_id": "r_g8gsmjLJgJ",
    "publication_info": {
        "summary": "VG Ashok, S Feng, Y Choi - … of the 2013 conference on empirical …, 2013 - aclanthology.org",
        "authors": [
            {
                "name": "VG Ashok",
                "author_id": "Of8dNP0AAAAJ",
                "url": "https://scholar.google.com/citations?user=Of8dNP0AAAAJ&hl=en&oi=sra"
            }
        ]
    },
    "resources": [
        {
            "file_format": "PDF",
            "title": "aclanthology.org",
            "url": "https://aclanthology.org/D13-1181.pdf"
        }
    ],
    "inline_links": {
        "cite_url": "https://scholar.google.com/scholar?q=info:r_g8gsmjLJgJ:scholar.google.com/&output=cite&scirp=4&hl=en",
        "cited_by": {
            "cites_id": "10965319278609103023",
            "total": 182,
            "url": "https://scholar.google.com/scholar?cites=10965319278609103023&as_sdt=2005&sciodt=0,5&hl=en"
        },
        "related_pages_url": "https://scholar.google.com/scholar?q=related:r_g8gsmjLJgJ:scholar.google.com/&scioq=best+novels&hl=en&as_sdt=0,5",
        "versions": {
            "cluster_id": "10965319278609103023",
            "total": 10,
            "url": "https://scholar.google.com/scholar?cluster=10965319278609103023&hl=en&as_sdt=0,5"
        }
    }
}
```

Key fields:

- `title`, `url`, `description` – core article data
- `result_type` – `book`, `pdf`, `html`, and similar
- `publication_info.authors` – author names with Google Scholar `author_id` and profile URLs
- `inline_links.cited_by.total` – citation count, with a URL to the citing articles
- `inline_links.cite_url` – link to the citation formats page
- `resources` – direct links to available PDF documents

## Final word

Check our [Google Scholar documentation](https://developers.oxylabs.io/api-targets/search-engines/google/scholar) for the full list of API parameters and response fields.

If you have any questions, feel free to contact us at support@oxylabs.io.

Read More Google Scraping Related Repositories: [Google Sheets for Basic Web Scraping](https://github.com/oxylabs/web-scraping-google-sheets), [Google Play Scraper](https://github.com/oxylabs/google-play-scraper), [How To Scrape Google Jobs](https://github.com/oxylabs/how-to-scrape-google-jobs), [Google News Scraper](https://github.com/oxylabs/google-news-scraper), [How to Scrape Google Flights with Python](https://github.com/oxylabs/how-to-scrape-google-flights), [How To Scrape Google Images](https://github.com/oxylabs/how-to-scrape-google-images), [Scrape Google Search Results](https://github.com/oxylabs/scrape-google-python), [Scrape Google Trends](https://github.com/oxylabs/how-to-scrape-google-trends)
