from src.vector_store import VectorStore

urls = [
    "https://sourceallies.com",
    "https://www.sourceallies.com/about-us/",
    "https://www.sourceallies.com/partner-with-us/",
    "https://www.sourceallies.com/what-we-do/",
    "https://www.sourceallies.com/meet-our-team",
    # "https://www.sourceallies.com/careers/",
    # "https://www.sourceallies.com/blog/index.html",
    # "https://www.sourceallies.com/ml"
]

for url in urls:
    VectorStore.embed_data(url)
