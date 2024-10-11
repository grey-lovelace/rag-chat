from langchain.vectorstores.pgvector import PGVector
from langchain_community.document_loaders import (
    DirectoryLoader,
    PyPDFLoader,
    UnstructuredURLLoader,
    JSONLoader
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from src.embedding_model import EmbeddingModel
from dotenv import load_dotenv
import os
import psycopg2
from psycopg2.extensions import connection


class VectorStore:
    _store: PGVector = None
    _db_connection: connection = None

    def connection_info():
        load_dotenv()

        return {
            "host": os.environ.get("PGVECTOR_HOST", "localhost"),
            "port": int(os.environ.get("PGVECTOR_PORT", "5432")),
            "database": os.environ.get("PGVECTOR_DATABASE", "postgres"),
            "user": os.environ.get("PGVECTOR_USER", "postgres"),
            "password": os.environ.get("PGVECTOR_PASSWORD", "postgres"),
        }

    @staticmethod
    def get_store() -> PGVector:
        if not VectorStore._store:
            load_dotenv()

            CONNECTION_STRING = PGVector.connection_string_from_db_params(
                driver=os.environ.get("PGVECTOR_DRIVER", "psycopg2"),
                **VectorStore.connection_info()
            )
            COLLECTION_NAME = "website_data_embeddings"

            print("Creating vector store")
            VectorStore._store = PGVector(
                collection_name=COLLECTION_NAME,
                connection_string=CONNECTION_STRING,
                embedding_function=EmbeddingModel.get_model(),
            )
        return VectorStore._store

    @staticmethod
    def get_db_conn() -> connection:
        if not VectorStore._db_connection:
            load_dotenv()

            VectorStore._db_connection = psycopg2.connect(
                **VectorStore.connection_info()
            )
        return VectorStore._db_connection

    @staticmethod
    def get_sources() -> list[str]:
        db_cursor = VectorStore.get_db_conn().cursor()
        try:
            db_cursor.execute(
                "Select distinct cmetadata ->> 'source' as source from langchain_pg_embedding"
            )
            sources_raw = db_cursor.fetchall()
            sources = [row[0] for row in sources_raw]
            sources.sort()
        except:
            print("Could not get sources.")
            return []
        return sources

    @staticmethod
    def delete_all_sources() -> None:
        print("DELETING ALL DATA")
        db_cursor = VectorStore.get_db_conn().cursor()
        db_cursor.execute("Delete from langchain_pg_embedding where 1=1")
        VectorStore.get_db_conn().commit()

    @staticmethod
    def embed_data(data_source: str) -> int:
        if data_source.startswith("http"):
            data = VectorStore._get_url_docs(data_source)
        else:
            data = VectorStore._get_pdf_docs(data_source)

        print(data)
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=400
        )
        docs = text_splitter.split_documents(data)
        print(len(docs))

        if docs:
            VectorStore.get_store().add_documents(docs)
        return len(docs)

    @staticmethod
    def _get_url_docs(url: list[str]) -> list[Document]:
        loaders = UnstructuredURLLoader(urls=[url])
        return loaders.load()

    @staticmethod
    def _get_pdf_docs(dir: str) -> list[Document]:
        new_data = []
        already_indexed_sources = VectorStore.get_sources()
        # pdfs
        loader = DirectoryLoader(dir, glob="./*.pdf", loader_cls=PyPDFLoader)
        data = loader.load()
        for doc in data:
            if doc.metadata["source"] not in already_indexed_sources:
                new_data.append(doc)
        # json
        loader = DirectoryLoader(dir, glob="./*.json", loader_cls=JSONLoader, loader_kwargs = {
            'jq_schema':'.[]',
            'metadata_func': metadata_func,
            'content_key': 'content'
        })
        data = loader.load()
        for doc in data:
            if doc.metadata["source"] not in already_indexed_sources:
                new_data.append(doc)
        return new_data

    # Define the metadata extraction function.
def metadata_func(record: dict, metadata: dict) -> dict:
    metadata["title"] = record.get("title")
    metadata["source"] = record.get("source")
    return metadata