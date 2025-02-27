import os
import warnings
from dotenv import load_dotenv
from langchain.schema.document import Document
from docling.document_converter import DocumentConverter
from langchain_community.document_loaders.firecrawl import FireCrawlLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.chains import ConversationalRetrievalChain
from langchain_core.prompts import PromptTemplate


warnings.filterwarnings("ignore")

load_dotenv()

def load_data(files_path):
    """
    Take a list of file paths and concatenate the text from each file into
    one string. The string is formatted with markdown headers and separated
    by a horizontal rule.
    
    Parameters
    ----------
    files_path : list
        List of file paths to be concatenated
    
    Returns
    -------
    str
        Concatenated string of all the text from the files in the list
    """
    print("🚀 Start Loading PDF Data")
    converter = DocumentConverter()
    full_text = ""
    
    for path in files_path:
        temp_file_path = os.path.join(os.getcwd(), path.name)
        with open(temp_file_path, "wb") as temp_file:
            temp_file.write(path.read())
        
        result = converter.convert(temp_file.name).document
        full_text += result.export_to_markdown()
        
        full_text += "\n\n" + "---" + "\n"
    print("🏁 Finish Loading Data")
        
    return [Document(page_content=full_text)]

def load_data_from_url(url):
    """
    Take a URL and use FireCrawl to scrape the web page and return a list of
    Document objects containing the scraped text.
    
    Parameters
    ----------
    url : str
        URL of the web page to scrape
    
    Returns
    -------
    list
        List of Document objects containing the scraped text
    """
    print("🚀 Start Loading URL Data")
    loader = FireCrawlLoader(url=url, mode="scrape", api_key=os.getenv("FIRE_CRAWEL_API"))
    data = loader.load()
    print("🏁 Finish Loading URL Data")
    return data

def create_index(index_name):
    """
    Create a Pinecone index with the given name if it doesn't already exist.

    This function is used to create an index in Pinecone if it doesn't already exist.

    Parameters
    ----------
    index_name : str
        The name of the index to create

    Returns
    -------
    index : pinecone.Index
        The created index object
    """
    pc = Pinecone()
    existing_indexes = [index_info["name"] for index_info in pc.list_indexes()]
    if index_name not in existing_indexes:
        pc.create_index(
            name=index_name,
            dimension=768,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1"),
        )
    index = pc.Index(index_name)


def create_vector_db(data):
    """
    Take a list of Document objects and create a Pinecone index with them, using
    the GoogleGenerativeAIEmbeddings model to create embeddings.
    
    Parameters
    ----------
    data : list
        List of Document objects to be indexed
    
    Returns
    -------
    PineconeVectorStore
        PineconeVectorStore object containing the indexed documents
    """
    print("🚩 Start Splitting ...")
    splitter = RecursiveCharacterTextSplitter(chunk_size=2000,
                                              chunk_overlap=200)
    doc = splitter.split_documents(data)
    
    # Initialize Embedding & Create Pinecone index
    print("🚩 Start Creating Vector DB ...")
    index_name = "rag-full-project"
    embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_db = PineconeVectorStore.from_documents(documents=doc, embedding=embedding, index_name=index_name)  
    print("✅ Finsh Creating Vector DB ...")  
    return vector_db



def create_retriever_chain(vectorstore):
    """
    Create a ConversationalRetrievalChain that uses the given vectorstore
    for retrieval and the gemini-2.0-flash-thinking-exp-01-21 model for
    generating answers.

    Parameters
    ----------
    vectorstore : PineconeVectorStore
        The PineconeVectorStore object to use for retrieval

    Returns
    -------
    ConversationalRetrievalChain
        A ConversationalRetrievalChain object with the specified retriever
        and llm
    """
    retriever = vectorstore.as_retriever(search_type="mmr", search_kwargs={"k": 5})
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-thinking-exp-01-21")

    template = """
    You are an AI research assistant specializing in research_field.  
    Your task is to answer questions about the research papers.  

    Use the following context from the paper to provide an accurate response in markdown format (highly structured):  
    {context}  

    Question: {question}  

    Answer the question strictly based on the provided context. If the context is insufficient, state that more information is needed.
    """

    prompt = PromptTemplate(
        input_variables=["context", "question"], 
        template=template
    )

    return ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        return_source_documents=True,
        combine_docs_chain_kwargs={"prompt": prompt, "document_variable_name": "context"},
    )


# def get_response(user_query, chat_history):
#     index_name = 'rag-full-project'
#     embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
#     vector_db = PineconeVectorStore(embedding=embedding, index_name=index_name)
#     load_qa_chain = create_retriever_chain(vectorstore=vector_db)
#     result = load_qa_chain.invoke(
#                 {
#                     "question": user_query,
#                     "chat_history": chat_history,
#                 }
#             )
    
#     return result