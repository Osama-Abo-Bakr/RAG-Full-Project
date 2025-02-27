# Full RAG Project

## Overview
The Full RAG Project is a Retrieval-Augmented Generation (RAG) application that allows users to upload PDFs or input URLs and retrieve relevant information using a conversational AI assistant. The system utilizes Pinecone for vector storage, FireCrawl for web scraping, and Google Generative AI for generating responses.

## Features
- Upload and process PDFs, DOCX, and PPTX documents.
- Extract and process data from web pages using FireCrawl.
- Store and retrieve documents efficiently using Pinecone.
- Generate responses based on retrieved documents using Google Generative AI.
- Interactive chatbot interface powered by Streamlit.

## Installation

### Prerequisites
Ensure you have Python installed (>=3.8). You also need an active Pinecone and Google Generative AI API key.

### Steps
1. Clone the repository:
   ```sh
   git clone https://github.com/Osama-Abo-Bakr/RAG-Full-Project
   cd RAG-Full-Project
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Set up environment variables:
   - Create a `.env` file in the root directory.
   - Copy contents from `.env.example` and add your API keys.

## Usage

### Running the Application
Execute the following command:
```sh
streamlit run main.py
```

### Interacting with the Chatbot
- Choose "PDF" to upload and process documents.
- Choose "URL" to fetch and process content from a web page.
- Enter queries in the chat interface to retrieve information.

## Project Structure
```
├── main.py              # Main Streamlit application
├── utils.py             # Utility functions for data processing
├── test.py              # Script to test the Pinecone index creation
├── requirements.txt     # Dependencies
├── .env.example         # Example environment variables file
├── .gitignore           # Git ignore file
```

## Technologies Used
- **Python**
- **Streamlit** (for UI)
- **LangChain** (for retrieval)
- **Pinecone** (for vector storage)
- **Google Generative AI** (for response generation)
- **FireCrawl** (for web scraping)

## License
This project is licensed under the MIT License.

## Author
[Osama Abo-Bakr](https://github.com/Osama-Abo-Bakr)