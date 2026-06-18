// components/Message.tsx
import React from "react";

export type MessageRole = "user" | "assistant" | "error";

export interface SourceData {
  preview: string;
}

export interface MessageData {
  id: string;
  role: MessageRole;
  content: string;
  sources?: SourceData[];
  confidence?: number;
  timestamp: Date;
}

interface MessageProps {
  message: MessageData;
}

function ConfidenceBadge({ value }: { value: number }) {
  const pct = Math.round(value * 100);

  const tier =
    pct >= 80 ? "high" : pct >= 55 ? "medium" : pct > 0 ? "low" : "none";

  const labels: Record<string, string> = {
    high: "High confidence",
    medium: "Medium confidence",
    low: "Low confidence",
    none: "No match",
  };

  return (
    <span className={`confidence-badge confidence-${tier}`}>
      {tier !== "none" && (
        <span className="confidence-bar">
          <span
            className="confidence-fill"
            style={{ width: `${pct}%` }}
          />
        </span>
      )}
      <span className="confidence-text">
        {labels[tier]}
        {tier !== "none" ? ` · ${pct}%` : ""}
      </span>
    </span>
  );
}

export const Message: React.FC<MessageProps> = ({ message }) => {
  const { role, content, sources = [], confidence } = message;

  const noInfo =
    role === "assistant" &&
    typeof confidence === "number" &&
    confidence === 0 &&
    sources.length === 0;

  return (
    <div className={`message-row message-${role}`}>
      {role !== "user" && (
        <div className="avatar avatar-ai" aria-hidden="true">
          {role === "error" ? "!" : "AI"}
        </div>
      )}

      <div className="message-bubble-group">
        <div className={`message-bubble bubble-${role}`}>
          <p className="message-text">
            {noInfo
              ? "No relevant information found in the document."
              : content}
          </p>

          {role === "assistant" && !noInfo && (
            <>
              {typeof confidence === "number" && (
                <div className="message-meta">
                  <ConfidenceBadge value={confidence} />
                </div>
              )}

              {sources.length > 0 && (
                <div className="sources-section">
                  <p className="sources-heading">
                    <svg
                      width="12"
                      height="12"
                      viewBox="0 0 12 12"
                      fill="none"
                      aria-hidden="true"
                    >
                      <rect
                        x="1"
                        y="1"
                        width="10"
                        height="10"
                        rx="1"
                        stroke="currentColor"
                        strokeWidth="1.2"
                      />
                      <path
                        d="M3 4h6M3 6h6M3 8h4"
                        stroke="currentColor"
                        strokeWidth="1.2"
                        strokeLinecap="round"
                      />
                    </svg>
                    Sources
                  </p>

                  <ul className="sources-list">
                    {sources.map((src, i) => (
                      <li key={i} className="source-item">
                        <span className="source-index">
                          {i + 1}
                        </span>

                        <span className="source-text">
                          {src.preview}
                        </span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </>
          )}
        </div>

        <span className="message-time">
          {new Date(message.timestamp).toLocaleTimeString([], {
            hour: "2-digit",
            minute: "2-digit",
          })}
        </span>
      </div>

      {role === "user" && (
        <div className="avatar avatar-user" aria-hidden="true">
          U
        </div>
      )}
    </div>
  );
};