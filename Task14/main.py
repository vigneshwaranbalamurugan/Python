import asyncio

from crawler import WebCrawler
from exporter import save_graph, save_sitemap
from config import get_config

async def main():
    config = get_config()
    crawler = WebCrawler(
        config.url,
        config.depth,
        config.concurrency
    )
    graph = await crawler.crawl()
    save_graph(graph)
    save_sitemap(graph.keys())
    print("\nCrawl Complete ✔")
    print("Broken links:", crawler.broken_links)
    print("Redirects:", crawler.redirects)

if __name__ == "__main__":
    asyncio.run(main())