from src.vector_store import store

def find(query: str):
    docs_with_scores = store.similarity_search_with_score(query)
    for doc, score in docs_with_scores:
        print("-" * 70)
        print("Score: ", score)
        print(doc.page_content)
        print("-" * 70)

find("Who were Source Allies's black belts this year?")