from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

def normalize_url(base, link):
    return urljoin(base, link)

def get_domain(url):
    return urlparse(url).netloc

def extract_links(html, base_url):
    soup = BeautifulSoup(html, "html.parser")
    links = set()
    for tag in soup.find_all("a", href=True):
        links.add(normalize_url(base_url, tag["href"]))
    return links