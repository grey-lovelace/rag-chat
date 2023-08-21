import streamlit as st
from src.llm import llm_chain
from embed_url import embed_url
from embed_pdf import embed_pdfs
from src.vector_store import db_conn
from src.get_vector_sources import get_vector_sources

def main():
    st.set_page_config(page_title="Rag Chat")

    # Initialize Session State
    if 'sources' not in st.session_state:
        st.session_state.sources = get_vector_sources()
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Sidebar
    def clear_indexed_data():
        print("DELETING ALL DATA")
        db_cursor = db_conn.cursor()
        db_cursor.execute("Delete from langchain_pg_embedding where 1=1")
        db_conn.commit()
        st.session_state.sources = []
    st.sidebar.button("Clear All Data", on_click=clear_indexed_data )

    st.sidebar.header("Already Loaded Data Sources")
    expander = st.sidebar.container()
    for source in st.session_state.sources:
        expander.write(source)


    # Add new data sources
    st.header("Load other data sources here...")
    def add_data_submit():
        if st.session_state.data_to_load_input != '':
            with st.spinner(f"loading \"{st.session_state.data_to_load_input}\""):
                if st.session_state.data_to_load_input.startswith("http"):
                    st.session_state.docs_found = embed_url(st.session_state.data_to_load_input)
                else:
                    st.session_state.docs_found = embed_pdfs(st.session_state.data_to_load_input)
            if st.session_state.docs_found > 0:
                st.session_state.sources = get_vector_sources()

            st.session_state.data_to_load_input = ''

    st.text_input("Anything starting with \"http(s)\" is assumed to be a website. Otherwise, it is assumed to be a directory on your computer that contains PDF files.", key="data_to_load_input", on_change=add_data_submit)
    webload_container = st.empty()
    if 'docs_found' in st.session_state:
        if st.session_state.docs_found == 0:
            webload_container.info("No info found.")
        else:
            webload_container.info("Info loaded!")


    # Ask LLM Questions
    st.header("...then ask questions about the contents here!")
    def query_submit():
        if st.session_state.query_input != '':
            st.session_state.messages = [
                {"role": "user", "content": st.session_state.query_input},
                {"role": "assistant", "content": "..."}
            ]
            with st.spinner(f"Finding an answer for \"{st.session_state.query_input}\"..."):
                st.session_state.result = llm_chain({"question": st.session_state.query_input})
            st.session_state.messages[1] = {"role": "assistant", "content": st.session_state.result["answer"]}
            st.session_state.query_input = ''
    st.text_input("Ask away!", key="query_input", on_change=query_submit)

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if __name__ == "__main__":
    main()