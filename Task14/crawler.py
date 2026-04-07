import asyncio
import aiohttp
from collections import defaultdict

from urls import extract_links
from robots_handler import RobotsHandler

class WebCrawler:
    def __init__(self, seed_url, max_depth, concurrency):
        self.seed = seed_url
        self.max_depth = max_depth
        self.visited = set()
        self.graph = defaultdict(list)
        self.sem = asyncio.Semaphore(concurrency)
        self.robots = RobotsHandler(seed_url)
        self.broken_links = []
        self.redirects = []

    async def fetch(self, session, url):
        async with self.sem:
            try:
                async with session.get(url) as response:
                    status = response.status
                    if status == 404:
                        self.broken_links.append(url)

                    if status in [301, 302]:
                        self.redirects.append(url)

                    html = await response.text()
                    print(f"{url} -> {status}")
                    return html
            except Exception:
                return ""

    async def crawl_level(self, session, urls, depth):
        next_level = set()
        tasks = []
        for url in urls:
            if url in self.visited:
                continue

            if not self.robots.allowed(url):
                continue

            self.visited.add(url)

            tasks.append(self.fetch(session, url))

        pages = await asyncio.gather(*tasks)
        for html, url in zip(pages, urls):
            if not html:
                continue
            links = extract_links(html, url)
            self.graph[url] = list(links)
            next_level.update(links)
        return next_level

    async def crawl(self):
        async with aiohttp.ClientSession() as session:
            current_level = {self.seed}
            for depth in range(self.max_depth + 1):
                print(f"\nDEPTH {depth}")
                current_level = await self.crawl_level(
                    session,
                    current_level,
                    depth
                )
        return self.graph