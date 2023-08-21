from src.vector_store import db_conn

def get_vector_sources():
    db_cursor = db_conn.cursor()
    db_cursor.execute("Select distinct cmetadata ->> 'source' as source from langchain_pg_embedding")
    sources_raw = db_cursor.fetchall()
    sources= [row[0] for row in sources_raw]
    sources.sort()
    return sources