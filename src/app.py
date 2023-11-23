import streamlit as st
from src.llm import LLM
from src.vector_store import VectorStore


def main():
    st.set_page_config(page_title="Rag Chat")

    # Initialize Session State
    if "sources" not in st.session_state:
        st.session_state.sources = VectorStore.get_sources()
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Sidebar
    def clear_indexed_data():
        VectorStore.delete_all_sources()
        st.session_state.sources = []

    st.sidebar.button("Clear All Data", on_click=clear_indexed_data)

    st.sidebar.header("Already Loaded Data Sources")
    sidebar_container = st.sidebar.container()
    for source in st.session_state.sources:
        sidebar_container.write(source)

    # Add new data sources
    st.header("Load other data sources here...")

    def add_data_submit():
        if st.session_state.data_to_load_input != "":
            with st.spinner(f'loading "{st.session_state.data_to_load_input}"'):
                st.session_state.docs_found = VectorStore.embed_data(
                    st.session_state.data_to_load_input
                )
            if st.session_state.docs_found > 0:
                st.session_state.sources = VectorStore.get_sources()

            st.session_state.data_to_load_input = ""

    st.text_input(
        'Anything starting with "http(s)" is assumed to be a website. Otherwise, it is assumed to be a directory on your computer that contains PDF files.',
        key="data_to_load_input",
        on_change=add_data_submit,
    )
    webload_container = st.empty()
    if "docs_found" in st.session_state:
        if st.session_state.docs_found == 0:
            webload_container.info("No info found.")
        else:
            webload_container.info("Info loaded!")

    # Ask LLM Questions
    st.header("...then ask questions about the contents here!")

    def query_submit():
        if st.session_state.query_input != "":
            st.session_state.messages = [
                {"role": "user", "content": st.session_state.query_input},
                {"role": "assistant", "content": "..."},
            ]
            with st.spinner(
                f'Finding an answer for "{st.session_state.query_input}"...'
            ):
                st.session_state.result = LLM.get_chain().invoke(
                    {"question": st.session_state.query_input}
                )
            st.session_state.messages[1] = {
                "role": "assistant",
                "content": st.session_state.result["answer"].content,
            }
            sourcebody = "SOURCES:\n\n" + "\n\n".join(
                list(
                    {
                        d.metadata["source"]
                        for d in st.session_state.result["context"]
                    }
                )
            )
            print(sourcebody)
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": sourcebody,
                }
            )
            st.session_state.query_input = ""

    st.text_input("Ask away!", key="query_input", on_change=query_submit)

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(cleanMessage(message["content"]))

def cleanMessage(message: str) -> str:
    return message.replace('$','\\$')


if __name__ == "__main__":
    main()
