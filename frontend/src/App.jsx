import { useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

function App() {
const [question, setQuestion] = useState("");
const [messages, setMessages] = useState([]);
const [loading, setLoading] = useState(false);
const [error, setError] = useState("");

const askQuestion = async (text) => {
const currentQuestion = (text ?? question).trim();
if (!currentQuestion || loading) return;

setMessages((prev) => [
  ...prev,
  { role: "user", content: currentQuestion },
]);

setQuestion("");
setError("");
setLoading(true);

try {
  const response = await fetch(`${API_URL}/ask`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ question: currentQuestion }),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Backend request failed.");
  }

  setMessages((prev) => [
    ...prev,
    {
      role: "assistant",
      content: data.answer || "The assistant returned an empty answer.",
    },
  ]);
} catch (err) {
  setError(err.message);

  setMessages((prev) => [
    ...prev,
    {
      role: "assistant",
      content:
        "I could not get a response from the backend. Please check that FastAPI is running on port 8000.\n\n" +
        `Error: ${err.message}`,
    },
  ]);
} finally {
  setLoading(false);
}
};

const handleSubmit = (event) => {
event.preventDefault();
askQuestion();
};

const clearChat = () => {
setMessages([]);
setQuestion("");
setError("");
};

return ( <div className="app-container"> <aside className="sidebar"> <div className="brand"> <div className="brand-icon">AI</div> <div> <h2>DocuMind</h2> <p>Intelligent Assistant</p> </div> </div>

    <div className="sidebar-section">
      <p className="section-label">YOUR WORKSPACE</p>

      <div className="sidebar-item active">
        <span>💬</span>
        AI Chat
      </div>

      <div className="sidebar-item">
        <span>📚</span>
        My Documents
      </div>
    </div>

    <div className="sidebar-bottom">
      <div className="connection-status">
        <span className="status-dot"></span>
        Backend configured
      </div>
      <p>Groq · FAISS · FastAPI</p>
    </div>
  </aside>

  <main className="main-content">
    <header className="topbar">
      <div>
        <h2>AI Document Assistant</h2>
        <p>Ask questions about your knowledge base</p>
      </div>

      <button
        type="button"
        className="clear-button"
        onClick={clearChat}
      >
        Clear Chat
      </button>
    </header>

    <section className="chat-area">
      {messages.length === 0 ? (
        <div className="welcome-screen">
          <div className="welcome-icon">✦</div>

          <h1>How can I help you today?</h1>

          <p>
            Ask questions about your documents and receive
            intelligent, context-aware answers.
          </p>

          <div className="suggestion-grid">
            {[
              "What is machine learning?",
              "Explain supervised learning.",
              "What is overfitting?",
              "Explain classification and regression.",
            ].map((item) => (
              <button
                type="button"
                key={item}
                className="suggestion-card"
                onClick={() => askQuestion(item)}
                disabled={loading}
              >
                {item}
                <span>↗</span>
              </button>
            ))}
          </div>
        </div>
      ) : (
        <div className="messages-container">
          {messages.map((message, index) => (
            <div
              className={`message-row ${message.role}`}
              key={index}
            >
              <div className="message-avatar">
                {message.role === "user" ? "U" : "AI"}
              </div>

              <div className="message-content">
                <div className="message-name">
                  {message.role === "user" ? "You" : "AI Assistant"}
                </div>

                <div className="markdown-body">
                  {message.role === "assistant" ? (
                    <ReactMarkdown remarkPlugins={[remarkGfm]}>
                      {message.content}
                    </ReactMarkdown>
                  ) : (
                    <p>{message.content}</p>
                  )}
                </div>
              </div>
            </div>
          ))}

          {loading && (
            <div className="message-row assistant">
              <div className="message-avatar">AI</div>

              <div className="message-content">
                <div className="message-name">AI Assistant</div>

                <div className="typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                  Thinking...
                </div>
              </div>
            </div>
          )}
        </div>
      )}
    </section>

    <footer className="input-section">
      <form className="chat-form" onSubmit={handleSubmit}>
        <input
          type="text"
          value={question}
          onChange={(event) => setQuestion(event.target.value)}
          placeholder="Ask anything about your documents..."
          disabled={loading}
          autoComplete="off"
        />

        <button
          type="submit"
          className="send-button"
          disabled={loading}
        >
          {loading ? "Sending..." : "Send ↑"}
        </button>
      </form>

      {error && (
        <p className="error-message">
          Backend error: {error}
        </p>
      )}

      <p className="footer-note">
        Powered by Groq LLM · FAISS · Hugging Face Embeddings · FastAPI
      </p>
    </footer>
  </main>
</div>
);
}

export default App;
