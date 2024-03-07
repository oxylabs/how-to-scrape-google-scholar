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
