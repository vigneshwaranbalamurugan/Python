# Concurrent Web Crawler with Depth Control
# Description
Build a web crawler that starts from a seed URL, extracts links,
and recursively crawls up to a configurable depth with concurrency,
deduplication, and robots.txt compliance.

# Use-Case:
- Accept a seed URL, max depth, and concurrency limit as CLI args
- Crawl pages level by level using async BFS
- Skip already-visited URLs and disallowed paths
- Log status codes and flag broken links (404), redirects (301/302)
- Identify orphan pages with zero inbound links
- Export the full link graph as JSON and a sitemap as XML