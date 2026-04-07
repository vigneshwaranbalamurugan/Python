import json

def save_graph(graph):
    with open("crawl_graph.json", "w") as f:
        json.dump(graph, f, indent=4)
    print("Graph saved ✔")

def save_sitemap(urls):
    with open("sitemap.xml", "w") as f:
        f.write("<urlset>\n")
        for url in urls:

            f.write(f"<url><loc>{url}</loc></url>\n")
        f.write("</urlset>")
    print("Sitemap saved")