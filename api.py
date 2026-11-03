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