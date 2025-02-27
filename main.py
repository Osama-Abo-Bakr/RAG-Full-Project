import streamlit as st
from dotenv import load_dotenv
from utils import (
    create_retriever_chain,
    create_vector_db,
    load_data,
    load_data_from_url
)

load_dotenv()

def setup_rag(data_source, data_key):
    """Handles session state initialization and retrieval chain setup."""
    if data_key not in st.session_state:
        st.session_state[data_key] = data_source()

    if "vector_db" not in st.session_state and st.session_state[data_key]:
        st.session_state.vector_db = create_vector_db(data=st.session_state[data_key])

    if "retriever_chain" not in st.session_state and st.session_state.vector_db:
        st.session_state.retriever_chain = create_retriever_chain(vectorstore=st.session_state.vector_db)

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

def chat_interface():
    """Handles chat input and response rendering."""
    user_query = st.chat_input("Enter your question:")
    if user_query and st.session_state.retriever_chain:
        result = st.session_state.retriever_chain.invoke({
            "question": user_query,
            "chat_history": st.session_state.chat_history,
        })
        st.session_state.chat_history.append((user_query, result["answer"].replace("```markdown", "").replace("```", "").strip()))

        for msg_u, msg_r in st.session_state.chat_history:
            with st.chat_message("user"):
                st.write(msg_u)
            with st.chat_message("assistant"):
                st.write(msg_r)

def main():
    st.set_page_config(page_title="Full RAG Project", page_icon="🚀", layout="wide")
    st.title("🚀 Full RAG Project")

    st.sidebar.header("Settings:")
    option = st.sidebar.radio("Choose Document Type", ["PDF", "URL"])

    if option == "URL":
        url_data = st.sidebar.text_input("Enter URL:")
        if url_data:
            setup_rag(lambda: load_data_from_url(url_data), "data")
            chat_interface()

    elif option == "PDF":
        pdf_data = st.sidebar.file_uploader("Upload Documents:", type=["pdf", "docx", "pptx", "doc"], accept_multiple_files=True)
        if pdf_data:
            setup_rag(lambda: load_data(files_path=pdf_data), "data")
            chat_interface()

if __name__ == "__main__":
    main()