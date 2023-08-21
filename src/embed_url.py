from src.vector_store import store
from langchain.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import CharacterTextSplitter

def embed_url(url: list[str]):
    loaders = UnstructuredURLLoader(urls=[url])
    data= loaders.load()
    print(data)

    text_splitter = CharacterTextSplitter(separator='\n', chunk_size=1000, chunk_overlap=200)
    docs = text_splitter.split_documents(data)
    print(len(docs))

    if docs:
        store.add_documents(docs)
    return len(docs)