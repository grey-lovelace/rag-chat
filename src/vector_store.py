from langchain.vectorstores.pgvector import PGVector
from langchain.embeddings import OpenAIEmbeddings
from dotenv import load_dotenv
import os
import psycopg2

load_dotenv()

db_conn = psycopg2.connect(
    database="postgres",
    host="localhost",
    user="postgres",
    password="postgres",
    port="5432"
)

CONNECTION_STRING = PGVector.connection_string_from_db_params(
    driver=os.environ.get("PGVECTOR_DRIVER", "psycopg2"),
    host=os.environ.get("PGVECTOR_HOST", "localhost"),
    port=int(os.environ.get("PGVECTOR_PORT", "5432")),
    database=os.environ.get("PGVECTOR_DATABASE", "postgres"),
    user=os.environ.get("PGVECTOR_USER", "postgres"),
    password=os.environ.get("PGVECTOR_PASSWORD", "postgres"),
)
COLLECTION_NAME = "website_data_embeddings"

print("Creating vector store")
embedding_model = OpenAIEmbeddings()
store = PGVector(
    collection_name=COLLECTION_NAME,
    connection_string=CONNECTION_STRING,
    embedding_function=embedding_model
)