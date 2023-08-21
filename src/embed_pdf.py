from vector_store import store
from langchain.document_loaders import DirectoryLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from get_vector_sources import get_vector_sources

def embed_pdfs(dir: str):
    already_indexed_sources = get_vector_sources()
    loader = DirectoryLoader(dir, glob = "./*.pdf", loader_cls = PyPDFLoader)
    data= loader.load()
    print(data)
    new_data = []
    for doc in data:
        if doc.metadata["source"] not in already_indexed_sources:
            new_data.append(doc)

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=400)
    docs = text_splitter.split_documents(new_data)

    if docs:
        store.add_documents(docs)
    return len(docs)