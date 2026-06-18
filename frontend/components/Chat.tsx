import React, { useState, useRef, useEffect, useCallback } from "react";
import { Upload } from "./Upload";
import { Message, MessageData, MessageRole } from "./Message";
import { InputBox } from "./InputBox";
import { queryDocument, ApiError } from "../services/api";

function makeMessage(
  role: MessageRole,
  content: string,
  extra?: Partial<MessageData>
): MessageData {
  return {
    id: crypto.randomUUID(), // safe (only used after mount)
    role,
    content,
    timestamp: new Date(), // use Date object (not string)
    ...extra,
  };
}

export const Chat: React.FC = () => {
  const [messages, setMessages] = useState<MessageData[]>([]);
  const [docId, setDocId] = useState<string | null>(null);
  const [input, setInput] = useState("");
  const [isQuerying, setIsQuerying] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [errorBanner, setErrorBanner] = useState<string | null>(null);

  const messagesEndRef = useRef<HTMLDivElement>(null);
  const chatBodyRef = useRef<HTMLDivElement>(null);

  // ✅ Initialize messages AFTER mount (prevents hydration mismatch)
  useEffect(() => {
    setMessages([
      {
        id: "welcome-msg",
        role: "assistant",
        content:
          "Hi! Upload a PDF and I'll answer any questions you have about it.",
        timestamp: new Date(),
        sources: [],
        confidence: undefined,
      },
    ]);
  }, []);

  // Scroll to bottom whenever messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const dismissError = () => setErrorBanner(null);

  const handleUploadSuccess = useCallback((id: string) => {
    setDocId(id);
    setErrorBanner(null);

    setMessages((prev) => [
      ...prev,
      makeMessage(
        "assistant",
        "Document indexed successfully! What would you like to know about it?",
        { sources: [], confidence: undefined }
      ),
    ]);
  }, []);

  const handleUploadError = useCallback((msg: string) => {
    setDocId(null);
    setErrorBanner(msg);
  }, []);

  const handleSubmit = useCallback(async () => {
    const query = input.trim();
    if (!query || !docId || isQuerying) return;

    setInput("");
    setErrorBanner(null);

    setMessages((prev) => [...prev, makeMessage("user", query)]);
    setIsQuerying(true);

    try {
      const history = messages
        .filter((m) => m.role === "user" || m.role === "assistant")
        .map((m) => ({ role: m.role as "user" | "assistant", content: m.content }));

      const response = await queryDocument({ query, doc_id: docId, history });
      setMessages((prev) => [
        ...prev,
        makeMessage("assistant", response.answer, {
          sources: response.sources ?? [],
          confidence: response.confidence ?? 0,
        }),
      ]);
    } catch (err) {
      const msg =
        err instanceof ApiError
          ? err.message
          : "Something went wrong. Please try again.";

      setMessages((prev) => [...prev, makeMessage("error", msg)]);
    } finally {
      setIsQuerying(false);
    }
  }, [input, docId, isQuerying]);

  return (
    <div className="chat-layout">
      {/* Sidebar */}
      <aside className="sidebar">
        <div className="sidebar-header">
          <span className="logo-mark">⬡</span>
          <span className="logo-text">DocMind</span>
        </div>

        <div className="sidebar-section">
          <p className="sidebar-label">Document</p>
          <Upload
            onUploadSuccess={handleUploadSuccess}
            onUploadError={handleUploadError}
            isUploading={isUploading}
            setIsUploading={setIsUploading}
            docId={docId}
          />

          {docId && (
            <p className="doc-id-tag">
              <span className="dot dot-green" />
              Indexed
            </p>
          )}
        </div>

        <div className="sidebar-section sidebar-tips">
          <p className="sidebar-label">Tips</p>
          <ul className="tips-list">
            <li>Ask specific questions for better answers</li>
            <li>Confidence score shows match quality</li>
            <li>Sources show relevant document passages</li>
          </ul>
        </div>
      </aside>

      {/* Main chat area */}
      <main className="chat-main">
        <header className="chat-header">
          <h1 className="chat-title">PDF Chat</h1>

          {docId && (
            <span className="status-pill">
              <span className="dot dot-green" />
              Ready
            </span>
          )}
        </header>

        {/* Error banner */}
        {errorBanner && (
          <div className="error-banner" role="alert">
            <span>⚠ {errorBanner}</span>
            <button
              className="error-dismiss"
              onClick={() => setErrorBanner(null)}
              aria-label="Dismiss error"
            >
              ×
            </button>
          </div>
        )}

        {/* Messages */}
        <div className="chat-body" ref={chatBodyRef}>
          {messages.map((msg) => (
            <Message key={msg.id} message={msg} />
          ))}

          {/* Typing indicator */}
          {isQuerying && (
            <div className="message-row message-assistant">
              <div className="avatar avatar-ai">AI</div>
              <div className="thinking-bubble">
                <span className="dot-flash" />
                <span
                  className="dot-flash"
                  style={{ animationDelay: "0.16s" }}
                />
                <span
                  className="dot-flash"
                  style={{ animationDelay: "0.32s" }}
                />
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Input */}
        <footer className="chat-footer">
          <InputBox
            value={input}
            onChange={setInput}
            onSubmit={handleSubmit}
            isLoading={isQuerying}
            disabled={!docId}
          />
        </footer>
      </main>
    </div>
  );
};