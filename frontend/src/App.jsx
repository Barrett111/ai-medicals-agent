import { useState } from "react";
import ReactMarkdown from "react-markdown";

function formatAnswer(data) {
  // If backend already sends string
  if (typeof data === "string") return data;

  // If backend sends nested object (your case)
  if (typeof data === "object") {
    let md = "";

    for (const section in data) {
      md += `## ${section}\n`;

      const content = data[section];

      if (typeof content === "string") {
        md += `- ${content}\n\n`;
      } else if (typeof content === "object") {
        for (const key in content) {
          const value = content[key];

          if (key === "bullet") {
            md += `- ${value}\n`;
          } else {
            md += `**${key}**: ${value}\n`;
          }
        }
        md += `\n`;
      }
    }

    return md;
  }

  return "Invalid response format";
}

function App() {
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const sendQuery = async () => {
    if (!query.trim()) return;

    const userMessage = { role: "user", text: query };
    setMessages((prev) => [...prev, userMessage]);

    setQuery("");
    setLoading(true);

    try {
      const res = await fetch("https://ai-medicals-agent-1.onrender.com/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ query }),
      });

      const data = await res.json();

      const botMessage = {
        role: "bot",
        text: formatAnswer(data.answer),
        confidence: data.confidence,
        source: data.source,
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      console.error("API Error:", error);

      setMessages((prev) => [
        ...prev,
        {
          role: "bot",
          text: "⚠️ Error connecting to backend.",
        },
      ]);
    }

    setLoading(false);
  };

  return (
    <div className="container">
      <h1>🧠 AI Medical Assistant</h1>

      <div className="chat">
        {messages.map((msg, i) => (
          <div key={i} className={`msg ${msg.role}`}>
            <ReactMarkdown>
              {typeof msg.text === "string"
                ? msg.text
                : JSON.stringify(msg.text, null, 2)}
            </ReactMarkdown>

            {msg.role === "bot" && msg.confidence !== undefined && (
              <div className="meta">
                <span>
                  Confidence: {(msg.confidence * 100).toFixed(0)}%
                </span>
                <span>Source: {msg.source}</span>
              </div>
            )}
          </div>
        ))}

        {loading && <div className="loading">AI is thinking...</div>}
      </div>

      <div className="inputBox">
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask medical question..."
          onKeyDown={(e) => e.key === "Enter" && sendQuery()}
        />
        <button onClick={sendQuery}>Send</button>
      </div>
    </div>
  );
}

export default App;