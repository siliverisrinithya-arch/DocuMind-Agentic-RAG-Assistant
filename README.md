DocuMind – Complete Project Reference & Source Bundle

This document consolidates the complete project documentation, configuration files, and Python source code for DocuMind: AI-Powered Agentic RAG Assistant with Multi-PDF Intelligence.

Part 1: README.md

# DocuMind – AI-Powered Agentic RAG Assistant with Multi-PDF Intelligence

## Overview
**DocuMind** is an AI-powered document intelligence application that enables users to interact with multiple PDF documents through natural language conversations. 

The platform combines Retrieval-Augmented Generation (RAG), semantic search, vector embeddings, and Agentic AI to retrieve relevant document information and generate context-aware responses. Instead of manually searching through lengthy documents, users can upload PDF files, ask questions, retrieve relevant information, and obtain precise AI-generated explanations.

The system uses a FastAPI backend and an interactive React frontend to provide an integrated document question-answering experience.

---

## Problem Statement
Traditional document analysis requires users to manually read, search, and compare large volumes of information across files. This process is time-consuming, prone to oversight, and inefficient—especially when navigating technical documentation, research papers, or business reports.

DocuMind addresses this challenge by providing an intelligent document retrieval and question-answering system that uses LLMs and RAG to make document knowledge accessible, structured, and conversational.

---

## Key Features
- **Multi-PDF Document Processing:** Load and process multiple PDF documents simultaneously.
- **Document Ingestion:** Extract clean textual information from PDF files using `PyPDFLoader`.
- **Intelligent Text Chunking:** Split documents into smaller, semantically coherent text segments with configurable chunk size and overlap.
- **Semantic Search:** Retrieve document chunks based on conceptual similarity rather than mere keyword matches.
- **Vector Embeddings:** Convert text into 384-dimensional dense vector representations via Hugging Face embedding models.
- **FAISS Vector Database:** Store and query document embeddings with high computational efficiency.
- **Retrieval-Augmented Generation (RAG):** Synthesize grounded responses backed directly by retrieved context to eliminate hallucinations.
- **Agentic AI & Tool Calling:** Use an autonomous AI agent equipped with document listing, semantic search, and document summarization tools.
- **Document Summarization:** Generate comprehensive overviews of long-form documents.
- **Conversational Question Answering:** Query documentation interactively using natural language.
- **REST API:** Expose core retrieval, ingestion, and agent execution pipelines via clean FastAPI endpoints.
- **Interactive Web Interface:** Access and inspect document workflows through a modern React (Vite) interface.

---

## System Architecture

```text
                 USER
                   │
                   ▼
             REACT FRONTEND
                   │
                   ▼
            FASTAPI BACKEND
                   │
                   ▼
           AGENTIC AI SYSTEM
                   │
          ┌────────┴────────┐
          ▼                 ▼
    DOCUMENT TOOLS      GROQ LLM
          │
          ▼
     RAG PIPELINE
          │
     ┌────┴─────┐
     ▼          ▼
 PDF LOADER   TEXT CHUNKING
     │          │
     └────┬─────┘
          ▼
     HUGGING FACE
      EMBEDDINGS
          │
          ▼
     FAISS VECTOR
       DATABASE
          │
          ▼
   SEMANTIC RETRIEVAL
          │
          ▼
   RETRIEVED CONTEXT
          │
          ▼
       GROQ LLM
          │
          ▼
  AI-GENERATED ANSWER
          │
          ▼
    USER RESPONSE


RAG Pipeline Stages

Document Ingestion: PDF files inside the storage directory are scanned, loaded, and parsed into page-level document objects.

Text Chunking: Pages are split using RecursiveCharacterTextSplitter (chunk size: 1000 characters, overlap: 150 characters) to preserve context continuity across boundaries.

Embedding Generation: Chunks are converted into vector representations using the sentence-transformers/all-MiniLM-L6-v2 model from Hugging Face.

Vector Database Creation: The dense embeddings are indexed into a local FAISS (Facebook AI Similarity Search) vector store for sub-millisecond similarity search.

Semantic Retrieval: When an incoming query arrives, FAISS performs top-$k$ cosine similarity search to fetch the most contextually relevant chunks.

Context-Aware Generation: Retrieved context and user prompts are passed to Groq-hosted open-weights LLMs to produce structured, fact-grounded responses.

Agentic AI Architecture

DocuMind extends baseline RAG into an autonomous agent paradigm. Rather than forcing every query down a static retrieval route, an LLM agent uses function calling to select from three specialized tools:

Tool Name

Purpose

Execution Logic

list_documents

Document Discovery

Returns filenames of all available PDFs stored in the knowledge base.

search_documents

Targeted Retrieval

Executes semantic vector search and returns top-$k$ relevant text chunks with source metadata.

summarize_document

Long-Form Synthesis

Retrieves broader document segments and synthesizes high-level summaries.

Technology Stack

Category

Technologies

Programming Language

Python, JavaScript (ES6+)

LLM Provider

Groq API

Orchestration & RAG

LangChain

Embedding Model

sentence-transformers/all-MiniLM-L6-v2

Vector Database

FAISS (CPU)

Document Processing

PyPDF

Backend Framework

FastAPI, Uvicorn

Data Validation

Pydantic

Frontend Framework

React.js, Vite

Styling

CSS

API Protocol

REST API

Version Control

Git, GitHub

Project Structure

rag_agentic_assistant/
│
├── data/                               # Uploaded and source PDF files
│   └── rag_sample_machine_learning.pdf
│
├── vectorstore/                        # Serialized local FAISS index files
│
├── frontend/                           # React frontend client
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── index.css
│   │   └── main.jsx
│   ├── package.json
│   └── index.html
│
├── agent.py                            # Agent loop, tool schema, and tool dispatcher
├── api.py                              # FastAPI routing and CORS configuration
├── rag_pipeline.py                     # Document loader, chunker, embeddings, and FAISS store
├── requirements.txt                    # Backend Python dependencies
├── .env                                # Local secrets (API keys)
├── .gitignore                          # Version control ignore definitions
└── README.md                           # Documentation


Note: .env, .venv, and the generated vectorstore/ index are explicitly excluded from version control via .gitignore.

Installation and Setup

Prerequisites

Python 3.10+ (Python 3.12 recommended)

Node.js (v18+) and npm

Git

Valid Groq API key

1. Clone the Repository

git clone https://github.com/siliverisrinithya-arch/DocuMind-Agentic-RAG-Assistant.git
cd DocuMind-Agentic-RAG-Assistant


2. Configure Python Virtual Environment

On Windows (PowerShell):

python -m venv .venv
.venv\Scripts\Activate.ps1


On Linux / macOS:

python3 -m venv .venv
source .venv/bin/activate


3. Install Python Dependencies

pip install --upgrade pip
pip install -r requirements.txt
pip install python-multipart


4. Configure Environment Variables

Create a .env file in the project root directory:

GROQ_API_KEY=your_groq_api_key_here


5. Add Initial Documents

Place any seed PDF files into the data/ folder:

data/sample_document.pdf


6. Start the FastAPI Backend Server

Run Uvicorn from the project root:

python -m uvicorn api:app --reload


Backend API: http://127.0.0.1:8000

Interactive Swagger Docs: http://127.0.0.1:8000/docs

7. Start the React Frontend Application

Open a new terminal window:

cd frontend
npm install
npm run dev


Frontend URL: http://localhost:5173

API Endpoints

Method

Endpoint

Description

GET

/

Application root status check.

GET

/health

Backend and service health verification.

GET

/documents

Lists all indexed and available PDF files.

POST

/upload

Multipart endpoint to upload new PDF files to data/.

POST

/ask

Submits user questions to the Agentic RAG pipeline.

GET

/about

Returns project metadata, architectural components, and tooling.

Example Use Cases

1. Concept Explanation

Question: "What is supervised learning? Explain with examples."

Behavior: The agent searches the vector store, retrieves relevant passages from indexed machine learning documents, and delivers a coherent explanation with source attribution.

2. Document Summarization

Question: "Summarize the important concepts covered in the uploaded document."

Behavior: The agent executes summarize_document, loads high-coverage chunks across the document, and provides a structured high-level summary.

3. Multi-Document Knowledge Retrieval

Question: "Compare the findings across my uploaded files."

Behavior: The RAG pipeline performs cross-document retrieval, comparing points across distinct sources without losing metadata traceability.

Security Considerations

Environment Isolation: API keys and sensitive tokens are read strictly from .env and never hardcoded.

Repository Safety: .gitignore actively excludes .env, Python cache, temporary test fixtures, virtual environments, and generated FAISS binaries.

Vector Serialization Security: allow_dangerous_deserialization=True is restricted to locally generated vector files.

Future Enhancements

Hybrid search combining dense semantic vectors and sparse lexical search (BM25).

Cross-encoder reranking (e.g., Cohere or BGE rerankers) to enhance top-$k$ precision.

Query rewriting and conversational memory persistence via Redis or SQLite.

Multi-agent orchestration using LangGraph.

Native citation rendering with highlighted PDF bounding-box coordinates.

Containerized multi-service deployment using Docker Compose.

Learning Outcomes

Designing end-to-end Retrieval-Augmented Generation workflows.

Implementing embedding generation and vector search utilizing FAISS.

Building tool-calling agent loops using Groq's low-latency inference endpoints.

Developing modular, production-structured REST APIs with FastAPI.

Integrating Python backend architectures with interactive modern React frontends.

Author

Siliveri Srinithya

Electrical and Electronics Engineering Student | AI/ML & Generative AI Enthusiast

GitHub: @siliverisrinithya-arch

LinkedIn: Srinithya Siliveri

License

This project is open-source and intended for educational and portfolio demonstration purposes.


---

# Part 2: Configuration & Environment

### `requirements.txt`
```text
fastapi
uvicorn
python-multipart
pydantic
python-dotenv
groq
langchain
langchain-community
langchain-huggingface
langchain-text-splitters
pypdf
faiss-cpu
sentence-transformers


.env

GROQ_API_KEY=your_groq_api_key_here


.gitignore

.env
.venv/
__pycache__/
*.pyc
vectorstore/
data/*.pdf
node_modules/
dist/
.DS_Store


Part 3: Backend Python Files

File 1: rag_pipeline.py

import os
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

# ==========================================
# 1. PROJECT CONFIGURATION
# ==========================================

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
VECTOR_DIR = BASE_DIR / "vectorstore"

DATA_DIR.mkdir(parents=True, exist_ok=True)

load_dotenv(BASE_DIR / ".env")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

MODEL_NAME = "openai/gpt-oss-120b"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env file.")

client = Groq(api_key=GROQ_API_KEY)


# ==========================================
# 2. LOAD PDF DOCUMENTS
# ==========================================

def load_pdf_documents():
    pdf_files = sorted(DATA_DIR.glob("*.pdf"))

    if not pdf_files:
        raise FileNotFoundError("No PDF files found in data folder.")

    documents = []

    print("\nLoading PDF documents...")

    for pdf_file in pdf_files:
        print("Reading:", pdf_file.name)

        loader = PyPDFLoader(str(pdf_file))
        pages = loader.load()

        documents.extend(pages)

        print("Pages loaded:", len(pages))

    print("\nTotal PDFs:", len(pdf_files))
    print("Total pages:", len(documents))

    return documents


# ==========================================
# 3. SPLIT DOCUMENTS
# ==========================================

def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150
    )

    chunks = splitter.split_documents(documents)

    print("\nTotal chunks:", len(chunks))

    if not chunks:
        raise ValueError("No readable text found in the PDF documents.")

    return chunks


# ==========================================
# 4. CREATE EMBEDDINGS
# ==========================================

def create_embeddings():
    print("\nLoading embedding model...")

    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True}
    )

    return embeddings


# ==========================================
# 5. CREATE FAISS DATABASE
# ==========================================

def create_vector_database(chunks, embeddings):
    print("\nCreating FAISS database...")

    vectorstore = FAISS.from_documents(
        documents=chunks,
        embedding=embeddings
    )

    VECTOR_DIR.mkdir(parents=True, exist_ok=True)
    vectorstore.save_local(str(VECTOR_DIR))

    print("FAISS database created successfully.")

    return vectorstore


# ==========================================
# 6. REBUILD FAISS AFTER PDF UPLOAD
# ==========================================

def rebuild_vector_database():
    print("\n================================")
    print("REBUILDING FAISS DATABASE")
    print("================================")

    documents = load_pdf_documents()
    chunks = split_documents(documents)
    embeddings = create_embeddings()
    vectorstore = create_vector_database(chunks, embeddings)

    print("\nAll PDF documents indexed successfully!")

    return vectorstore


# ==========================================
# 7. LOAD EXISTING FAISS DATABASE
# ==========================================

def load_vector_database():
    embeddings = create_embeddings()
    index_file = VECTOR_DIR / "index.faiss"

    if not index_file.exists():
        print("\nNo existing FAISS database found.")
        return rebuild_vector_database()

    print("\nLoading existing FAISS database...")

    vectorstore = FAISS.load_local(
        str(VECTOR_DIR),
        embeddings,
        allow_dangerous_deserialization=True
    )

    print("FAISS database loaded successfully.")

    return vectorstore


# ==========================================
# 8. REWRITE FOLLOW-UP QUESTIONS
# ==========================================

def rewrite_question(question, chat_history):
    if not chat_history:
        return question

    history_text = ""

    for message in chat_history[-6:]:
        history_text += f"{message['role']}: {message['content']}\n"

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": """
                Rewrite the user's latest question as a standalone
                question using the conversation history.

                Preserve the original meaning.
                Return only the rewritten question.
                If no rewriting is needed, return the original question.
                """
            },
            {
                "role": "user",
                "content": f"""
                Conversation history:
                {history_text}

                Latest question:
                {question}
                """
            }
        ],
        max_completion_tokens=200
    )

    rewritten = response.choices[0].message.content.strip()

    return rewritten or question


# ==========================================
# 9. SEARCH DOCUMENTS
# ==========================================

def search_documents(vectorstore, question):
    results = vectorstore.similarity_search(
        question,
        k=3
    )

    return results


# ==========================================
# 10. GENERATE ANSWERS WITH MEMORY
# ==========================================

def generate_answer(vectorstore, question, chat_history):
    search_question = rewrite_question(question, chat_history)

    print("\nSearching for:", search_question)

    results = search_documents(vectorstore, search_question)

    if not results:
        return (
            "I could not find relevant information in the documents.",
            []
        )

    context_parts = []
    sources = []

    for index, doc in enumerate(results):
        document_name = Path(
            doc.metadata.get("source", "Unknown")
        ).name

        page_number = int(doc.metadata.get("page", 0)) + 1

        context_parts.append(
            f"""
            Source {index + 1}
            Document: {document_name}
            Page: {page_number}
            Content:
            {doc.page_content}
            """
        )

        sources.append({
            "document": document_name,
            "page": page_number,
            "content": doc.page_content
        })

    context = "\n\n".join(context_parts)

    messages = [
        {
            "role": "system",
            "content": """
            You are an intelligent document-based RAG assistant.

            Answer using the retrieved document context and
            conversation history.

            Rules:
            1. Use document context as your evidence.
            2. Do not invent facts.
            3. If information is unavailable, say so.
            4. Understand follow-up questions using conversation history.
            5. Give clear and structured answers.
            """
        }
    ]

    messages.extend(chat_history[-6:])

    messages.append({
        "role": "user",
        "content": f"""
        Retrieved document context:

        {context}

        User question:

        {question}

        Answer using the retrieved context.
        """
    })

    print("\nGenerating AI answer...")

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        max_completion_tokens=1000
    )

    answer = response.choices[0].message.content

    return answer, sources


# ==========================================
# 11. MAIN ASSISTANT
# ==========================================

def run_rag_assistant():
    print("\n================================")
    print("RAG AGENTIC AI ASSISTANT")
    print("================================")

    vectorstore = rebuild_vector_database()

    chat_history = []

    print("\nAssistant is ready!")
    print("Ask questions about your PDF documents.")
    print("Type 'exit' to stop.")
    print("Type 'clear' to clear conversation memory.")

    while True:
        question = input("\nYou: ").strip()

        if question.lower() == "exit":
            print("\nThank you for using the assistant!")
            break

        if question.lower() == "clear":
            chat_history.clear()
            print("\nConversation memory cleared.")
            continue

        if not question:
            print("Please enter a question.")
            continue

        try:
            answer, sources = generate_answer(
                vectorstore,
                question,
                chat_history
            )

            print("\nAI Assistant:")
            print(answer)

            print("\nSource References:")
            for source in sources:
                print(
                    f"Document: {source['document']} | "
                    f"Page: {source['page']}"
                )

            chat_history.append({
                "role": "user",
                "content": question
            })

            chat_history.append({
                "role": "assistant",
                "content": answer
            })

            chat_history = chat_history[-6:]

        except Exception as error:
            print("\nError:", error)


if __name__ == "__main__":
    run_rag_assistant()


File 2: agent.py

import json
import os
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq

from rag_pipeline import (
    create_embeddings,
    create_vector_database,
    load_pdf_documents,
    load_vector_database,
    rebuild_vector_database,
    split_documents,
)

# =====================================================
# 1. CONFIGURATION
# =====================================================

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

load_dotenv(BASE_DIR / ".env")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = "openai/gpt-oss-120b"

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY missing in .env file")

client = Groq(api_key=GROQ_API_KEY)

# =====================================================
# 2. INITIALIZE RAG DATABASE
# =====================================================

print("\nInitializing Agentic AI Assistant...")
vectorstore = load_vector_database()
print("\nRAG database initialized successfully!")

# =====================================================
# 3. REFRESH DATABASE AFTER PDF UPLOAD
# =====================================================

def refresh_vector_database():
    global vectorstore

    print("\nRefreshing FAISS database...")
    vectorstore = rebuild_vector_database()
    print("\nFAISS database refreshed successfully!")

    return {
        "success": True,
        "message": "FAISS database updated successfully."
    }

# =====================================================
# 4. TOOL 1 - LIST DOCUMENTS
# =====================================================

def list_documents():
    pdf_files = sorted(DATA_DIR.glob("*.pdf"))

    if not pdf_files:
        return []

    return [file.name for file in pdf_files]

# =====================================================
# 5. TOOL 2 - SEARCH DOCUMENTS
# =====================================================

def search_documents(query):
    results = vectorstore.similarity_search(query, k=3)

    if not results:
        return "No relevant information found."

    output = ""
    for index, doc in enumerate(results, start=1):
        filename = Path(doc.metadata.get("source", "Unknown")).name
        page = int(doc.metadata.get("page", 0)) + 1

        output += f"""
Result {index}
Document: {filename}
Page: {page}
Content:
{doc.page_content}
"""
    return output

# =====================================================
# 6. TOOL 3 - SUMMARIZE DOCUMENTS
# =====================================================

def summarize_document(query):
    results = vectorstore.similarity_search(query, k=6)

    if not results:
        return "No relevant content available to summarize."

    context = "\n\n".join(doc.page_content for doc in results)

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": """
                You are a document summarization assistant.

                Summarize the supplied document information.
                Use only the supplied content.
                Do not invent facts.
                """
            },
            {
                "role": "user",
                "content": f"Summarize this information:\n{context}"
            }
        ],
        max_completion_tokens=700
    )

    return response.choices[0].message.content

# =====================================================
# 7. DEFINE AI TOOLS
# =====================================================

tools = [
    {
        "type": "function",
        "function": {
            "name": "list_documents",
            "description": "List all PDF documents uploaded by the user.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_documents",
            "description": "Search uploaded PDFs for relevant information.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Information to search for."
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "summarize_document",
            "description": "Summarize information from uploaded PDF documents.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Topic or subject to summarize."
                    }
                },
                "required": ["query"]
            }
        }
    }
]

# =====================================================
# 8. EXECUTE SELECTED TOOLS
# =====================================================

def execute_tool(tool_name, arguments):
    if tool_name == "list_documents":
        return json.dumps(list_documents())

    elif tool_name == "search_documents":
        return search_documents(arguments["query"])

    elif tool_name == "summarize_document":
        return summarize_document(arguments["query"])

    return "Unknown tool requested."

# =====================================================
# 9. AGENT DECISION-MAKING
# =====================================================

def run_agent(user_question):
    messages = [
        {
            "role": "system",
            "content": """
            You are an intelligent Agentic AI document assistant.

            You have three tools:

            1. list_documents:
               Lists uploaded PDF documents.

            2. search_documents:
               Searches for relevant information in PDFs.

            3. summarize_document:
               Summarizes information from PDFs.

            Decide which tool is appropriate for the user's request.

            Use the tools when necessary.
            After receiving tool results, provide a clear answer.

            Never invent document information.
            """
        },
        {
            "role": "user",
            "content": user_question
        }
    ]

    for step in range(5):
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            tools=tools,
            tool_choice="auto",
            max_completion_tokens=1500
        )

        assistant_message = response.choices[0].message

        if not assistant_message.tool_calls:
            return assistant_message.content or "No response generated."

        messages.append(assistant_message)

        for tool_call in assistant_message.tool_calls:
            tool_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)

            print(f"\nAgent selected tool: {tool_name}")
            print("Executing tool...")

            result = execute_tool(tool_name, arguments)

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(result)
            })

    return "The agent reached its maximum tool-call steps."

# =====================================================
# 10. MAIN PROGRAM
# =====================================================

def main():
    print("\n======================================")
    print("     AGENTIC AI DOCUMENT ASSISTANT")
    print("======================================")

    print("\nAvailable tools:")
    print("1. Document Search")
    print("2. Document Listing")
    print("3. Document Summarization")

    print("\nAsk questions about your uploaded PDFs.")
    print("Type 'exit' to stop.")

    while True:
        question = input("\nYou: ").strip()

        if question.lower() == "exit":
            print("\nAgentic AI Assistant stopped.")
            break

        if not question:
            print("Please enter a question.")
            continue

        try:
            answer = run_agent(question)
            print("\nAI Agent:")
            print(answer)

        except Exception as error:
            print("\nError:", error)


if __name__ == "__main__":
    main()


File 3: api.py

import shutil
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from agent import list_documents, run_agent

# 1. Initialize FastAPI

app = FastAPI(
    title="Agentic AI Document Assistant API",
    description="Backend API for a RAG-based Agentic AI Assistant",
    version="1.0.0",
)

# 2. Enable CORS

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. PDF storage folder

DATA_DIR = Path("data")
DATA_DIR.mkdir(parents=True, exist_ok=True)

# 4. Request model


class QuestionRequest(BaseModel):
    question: str = Field(min_length=1, max_length=2000)


# 5. Home endpoint


@app.get("/")
def home():
    return {
        "message": "Welcome to Agentic AI Assistant API",
        "status": "Running successfully",
    }


# 6. Health check endpoint


@app.get("/health")
def health_check():
    return {"status": "healthy"}


# 7. Get document list


@app.get("/documents")
def get_documents():
    try:
        documents = list_documents()
        return {"success": True, "documents": documents}
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))


# 8. Upload PDF endpoint


@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400, detail="Only PDF files are allowed."
        )

    safe_filename = Path(file.filename).name
    destination = DATA_DIR / safe_filename

    try:
        with destination.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return {
            "success": True,
            "message": "PDF uploaded successfully. Rebuild the document index before asking questions about it.",
            "filename": safe_filename,
        }
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))
    finally:
        await file.close()


# 9. Ask question endpoint


@app.post("/ask")
def ask_question(request: QuestionRequest):
    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400, detail="Question cannot be empty."
        )

    try:
        answer = run_agent(question)
        return {"success": True, "question": question, "answer": answer}
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))


# 10. Project information endpoint


@app.get("/about")
def about():
    return {
        "project": "RAG-Based Agentic AI Assistant",
        "technologies": [
            "Python",
            "LangChain",
            "FAISS",
            "Hugging Face Embeddings",
            "Groq LLM",
            "FastAPI",
            "React",
        ],
        "features": [
            "PDF document upload",
            "Semantic search",
            "AI question answering",
            "Agentic AI tools",
            "Document summarization",
            "REST API integration",
        ],
    }
## Application Screenshots

| Chat & Q&A Interface | PDF Upload & Processing |
| :---: | :---: |
| ![Chat UI](assets/ui_chat_interface.png) |<img width="1915" height="903" alt="image" src="https://github.com/user-attachments/assets/0b5d81e8-acc2-46c8-916b-bd7aa4ff05f5" />


| FastAPI Swagger Endpoints | Terminal Agent Trace |
| :---: | :---: |
| ![Swagger Docs](assets/swagger_api_docs.png) |<img width="1911" height="952" alt="image" src="https://github.com/user-attachments/assets/d755593f-a2dd-4521-b200-62f877e39295" />
<img width="1910" height="930" alt="image" src="https://github.com/user-attachments/assets/06abade6-8087-4f8c-b418-eecf9b75bc65" />
