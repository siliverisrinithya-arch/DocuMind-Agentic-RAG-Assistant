import os

from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("Groq API key not found!")

# Initialize Groq client
client = Groq(api_key=api_key)

# Send a test request
response = client.chat.completions.create(

    model ="openai/gpt-oss-120b",

    messages=[
        {
            "role": "system",
            "content": "You are a helpful AI assistant."
        },

        {
            "role": "user",
            "content": "Explain RAG in simple words."
        }
    ]
)

# Display response
print(response.choices[0].message.content)