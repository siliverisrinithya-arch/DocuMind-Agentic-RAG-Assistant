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
def list_documents():
    """Return the names of all PDF documents in the data folder."""
    from pathlib import Path

    data_dir = Path("data")
    data_dir.mkdir(parents=True, exist_ok=True)

    pdf_files = list(data_dir.glob("*.pdf"))

    return [file.name for file in pdf_files]