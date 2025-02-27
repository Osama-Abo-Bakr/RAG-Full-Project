import streamlit as st
from dotenv import load_dotenv
from utils import (create_retriever_chain,
                   create_vector_db,
                   load_data,
                   load_data_from_url,
                   create_index)


load_dotenv()


def main():
    st.set_page_config(page_title="Full RAG Project", page_icon="🚀", layout='wide')
    st.title("🚀 Full RAG Project")
    
    st.sidebar.header("Sitting: ")
    option = st.sidebar.radio(label="Choise type of Doc", options=["PDF's", "URL"])
    if option == "URL":
        # st.experimental_rerun()
        url_data = st.sidebar.text_input("Enter URL: ")
        if url_data:
            if "data" not in st.session_state:
                st.session_state.data = load_data_from_url(url=url_data)
            
            if "vector_db" not in st.session_state and st.session_state.data:
                st.session_state.vector_db = create_vector_db(data=st.session_state.data)
            
            if "retriver_chain" not in st.session_state and st.session_state.vector_db:
                st.session_state.retriver_chain = create_retriever_chain(vectorstore=st.session_state.vector_db)
                
            if "chat_history" not in st.session_state:
                st.session_state.chat_history = []
                
            
            user_query = st.chat_input("Enter the input: ")
            if user_query and st.session_state.retriver_chain:
                result = st.session_state.retriver_chain.invoke(
                    {
                        "question": user_query,
                        "chat_history": st.session_state.chat_history,
                    }
                )
                
                st.session_state.chat_history.append((user_query, result['answer'].replace("```markdown", "").replace("```", "").strip()))
                
                for (msg_u, msg_r) in st.session_state.chat_history:
                    with st.chat_message('user'):
                        st.write(msg_u)
                    with st.chat_message('assistant'):
                        st.write(msg_r)
            
            
            
        
    
    elif option == "PDF's":
        # st.experimental_rerun()
        
        pdf_data = st.sidebar.file_uploader("Enter URL: ", type=["pdf", "docx", "pptx", "doc"], accept_multiple_files=True)
        if pdf_data:
            if "data" not in st.session_state:
                st.session_state.data = load_data(files_path=pdf_data)
            
            if "vector_db" not in st.session_state and st.session_state.data:
                st.session_state.vector_db = create_vector_db(data=st.session_state.data)
            
            if "retriver_chain" not in st.session_state and st.session_state.vector_db:
                st.session_state.retriver_chain = create_retriever_chain(vectorstore=st.session_state.vector_db)
                
            if "chat_history" not in st.session_state:
                st.session_state.chat_history = []
                
            
            user_query = st.chat_input("Enter the input: ")
            if user_query and st.session_state.retriver_chain:
                result = st.session_state.retriver_chain.invoke(
                    {
                        "question": user_query,
                        "chat_history": st.session_state.chat_history,
                    }
                )
                
                st.session_state.chat_history.append((user_query, result['answer'].replace("```markdown", "").replace("```", "").strip()))
                
                for (msg_u, msg_r) in st.session_state.chat_history:
                    with st.chat_message('user'):
                        st.write(msg_u)
                    with st.chat_message('assistant'):
                        st.write(msg_r)
                
            
        
    else: pass
        
        
        
if __name__ == "__main__":
    main()