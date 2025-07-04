import React, { useState } from "react";
import "./App.css";

function App() {
  const [intent, setIntent] = useState("");
  const [tone, setTone] = useState("professional");
  const [length, setLength] = useState("medium");
  const [senderName, setSenderName] = useState("");
  const [receiverName, setReceiverName] = useState("");
  const [email, setEmail] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const generateEmail = async () => {
    if (!intent.trim() || !senderName.trim() || !receiverName.trim()) {
      alert("Please fill in all required fields!");
      return;
    }

    setIsLoading(true);
    try {
      const backendUrl = process.env.REACT_APP_BACKEND_URL || "http://localhost:8000";
      const res = await fetch(`${backendUrl}/generate-email`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
          intent, 
          tone, 
          length, 
          sender_name: senderName,
          receiver_name: receiverName
        }),
      });
      const data = await res.json();
      setEmail(data.email);
    } catch (error) {
      console.error("Error generating email:", error);
      alert("Failed to generate email. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  const copyToClipboard = () => {
    navigator.clipboard.writeText(email);
    alert("Email copied to clipboard!");
  };

  return (
    <div className="app">
      <div className="container">
        <header className="header">
          <h1>📧 AI Email Writer</h1>
          <p>Generate professional emails with AI assistance</p>
        </header>

        <div className="form-section">
          <div className="form-grid">
            <div className="form-group">
              <label>Your Name (Sender) *</label>
              <input
                type="text"
                placeholder="e.g., John Smith"
                value={senderName}
                onChange={(e) => setSenderName(e.target.value)}
                className="form-input"
              />
            </div>

            <div className="form-group">
              <label>Recipient Name *</label>
              <input
                type="text"
                placeholder="e.g., Sarah Johnson"
                value={receiverName}
                onChange={(e) => setReceiverName(e.target.value)}
                className="form-input"
              />
            </div>
          </div>

          <div className="form-group">
            <label>Email Intent *</label>
            <textarea
              placeholder="Describe what you want to achieve with this email (e.g., request a meeting, follow up on project, thank you note, etc.)"
              value={intent}
              onChange={(e) => setIntent(e.target.value)}
              className="form-textarea"
              rows="3"
            />
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Tone</label>
              <select value={tone} onChange={(e) => setTone(e.target.value)} className="form-select">
                <option value="professional">Professional</option>
                <option value="friendly">Friendly</option>
                <option value="formal">Formal</option>
                <option value="casual">Casual</option>
                <option value="enthusiastic">Enthusiastic</option>
                <option value="apologetic">Apologetic</option>
              </select>
            </div>

            <div className="form-group">
              <label>Length</label>
              <select value={length} onChange={(e) => setLength(e.target.value)} className="form-select">
                <option value="short">Short</option>
                <option value="medium">Medium</option>
                <option value="long">Long</option>
              </select>
            </div>
          </div>

          <button
            onClick={generateEmail}
            disabled={isLoading}
            className="generate-btn"
          >
            {isLoading ? "Generating..." : "✨ Generate Email"}
          </button>
        </div>

        {email && (
          <div className="result-section">
            <div className="result-header">
              <h3>Generated Email</h3>
              <button onClick={copyToClipboard} className="copy-btn">
                📋 Copy
              </button>
            </div>
            <div className="email-content">
              <pre>{email}</pre>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
