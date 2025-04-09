# How to Scrape Google Scholar

[![Oxylabs promo code](https://raw.githubusercontent.com/oxylabs/how-to-scrape-google-scholar/refs/heads/main/Google-Scraper-API-1090x275.png)](https://oxylabs.go2cloud.org/aff_c?offer_id=7&aff_id=877&url_id=112)

[![](https://dcbadge.vercel.app/api/server/eWsVUJrnG5)](https://discord.gg/Pds3gBmKMH)

Take a look at the process of getting titles, authors, and citations from [Google Scholar](https://scholar.google.com/) using Oxylabs [SERP Scraper API](https://oxylabs.io/products/scraper-api/serp) (a part of Web Scraper API) and Python. You can get a **1-week free trial** by registering on the [dashboard](https://dashboard.oxylabs.io/).

For a detailed walkthrough with explanations and visuals, check our [blog post](https://oxylabs.io/blog/how-to-scrape-google-scholar).
Also, do not hesitate to check this [Best SERP APIs](https://medium.com/@oxylabs.io/the-10-best-serp-apis-in-2024-22bf7f91f8f0) list 
## The complete code

```python
import requests
from bs4 import BeautifulSoup


USERNAME = "USERNAME"
PASSWORD = "PASSWORD"


def get_html_for_page(url):
    payload = {
        "url": url,
        "source": "google",
    }
    response = requests.post(
        "https://realtime.oxylabs.io/v1/queries",
        auth=(USERNAME, PASSWORD),
        json=payload,
    )
    response.raise_for_status()
    return response.json()["results"][0]["content"]


def get_citations(article_id):
    url = f"https://scholar.google.com/scholar?q=info:{article_id}:scholar.google.com&output=cite"
    html = get_html_for_page(url)
    soup = BeautifulSoup(html, "html.parser")
    data = []
    for citation in soup.find_all("tr"):
        title = citation.find("th", {"class": "gs_cith"}).get_text(strip=True)
        content = citation.find("div", {"class": "gs_citr"}).get_text(strip=True)
        entry = {
            "title": title,
            "content": content,
        }
        data.append(entry)

    return data


def parse_data_from_article(article):
    title_elem = article.find("h3", {"class": "gs_rt"})
    title = title_elem.get_text()
    title_anchor_elem = article.select("a")[0]
    url = title_anchor_elem["href"]
    article_id = title_anchor_elem["id"]
    authors = article.find("div", {"class": "gs_a"}).get_text()
    return {
        "title": title,
        "authors": authors,
        "url": url,
        "citations": get_citations(article_id),
    }


def get_url_for_page(url, page_index):
    return url + f"&start={page_index}"


def get_data_from_page(url):
    html = get_html_for_page(url)
    soup = BeautifulSoup(html, "html.parser")
    articles = soup.find_all("div", {"class": "gs_ri"})
    return [parse_data_from_article(article) for article in articles]


data = []
url = "https://scholar.google.com/scholar?q=global+warming+&hl=en&as_sdt=0,5"

NUM_OF_PAGES = 1
page_index = 0
for _ in range(NUM_OF_PAGES):
    page_url = get_url_for_page(url, page_index)
    entries = get_data_from_page(page_url)
    data.extend(entries)
    page_index += 10

print(data)
```

## Final word

Check our [documentation](https://developers.oxylabs.io/scraper-apis/web-scraper-api/google) for more API parameters and variables found in this tutorial.

If you have any questions, feel free to contact us at support@oxylabs.io.

Read More Google Scraping Related Repositories: [Google Sheets for Basic Web Scraping](https://github.com/oxylabs/web-scraping-google-sheets), [How to Scrape Google Shopping Results](https://github.com/oxylabs/scrape-google-shopping), [Google Play Scraper](https://github.com/oxylabs/google-play-scraper), [How To Scrape Google Jobs](https://github.com/oxylabs/how-to-scrape-google-jobs), [Google News Scrpaer](https://github.com/oxylabs/google-news-scraper), [How to Scrape Google Flights with Python](https://github.com/oxylabs/how-to-scrape-google-flights), [How To Scrape Google Images](https://github.com/oxylabs/how-to-scrape-google-images), [Scrape Google Search Results](https://github.com/oxylabs/scrape-google-python), [Scrape Google Trends](https://github.com/oxylabs/how-to-scrape-google-trends)
