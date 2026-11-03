import json
import os
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq

from rag_pipeline import (
    create_embeddings,
    create_vector_database,
    list_documents as list_docs_pipeline,
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