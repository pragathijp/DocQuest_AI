// components/InputBox.tsx
import React, { useRef, useEffect } from "react";

interface InputBoxProps {
  value: string;
  onChange: (value: string) => void;
  onSubmit: () => void;
  isLoading: boolean;
  disabled: boolean;
  placeholder?: string;
}

export const InputBox: React.FC<InputBoxProps> = ({
  value,
  onChange,
  onSubmit,
  isLoading,
  disabled,
  placeholder = "Ask a question about your PDF…",
}) => {
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Auto-resize textarea
  useEffect(() => {
    const ta = textareaRef.current;
    if (!ta) return;
    ta.style.height = "auto";
    ta.style.height = `${Math.min(ta.scrollHeight, 160)}px`;
  }, [value]);

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      if (!disabled && !isLoading && value.trim()) {
        onSubmit();
      }
    }
  };

  const canSubmit = !disabled && !isLoading && value.trim().length > 0;

  return (
    <div className="inputbox-wrapper">
      <div className={`inputbox-container ${disabled ? "inputbox-disabled" : ""}`}>
        <textarea
          ref={textareaRef}
          className="inputbox-textarea"
          value={value}
          onChange={(e) => onChange(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder={
            disabled ? "Upload a PDF to start asking questions…" : placeholder
          }
          disabled={disabled || isLoading}
          rows={1}
          aria-label="Chat input"
        />

        <button
          className={`send-button ${canSubmit ? "send-button-active" : ""}`}
          onClick={onSubmit}
          disabled={!canSubmit}
          aria-label="Send message"
        >
          {isLoading ? (
            <span className="send-spinner" />
          ) : (
            <svg
              width="18"
              height="18"
              viewBox="0 0 18 18"
              fill="none"
              aria-hidden="true"
            >
              <path
                d="M15.5 9L2.5 2.5L5.5 9L2.5 15.5L15.5 9Z"
                fill="currentColor"
                stroke="currentColor"
                strokeWidth="1"
                strokeLinejoin="round"
              />
            </svg>
          )}
        </button>
      </div>

      <p className="inputbox-hint">
        {isLoading
          ? "Thinking…"
          : "Press Enter to send · Shift+Enter for new line"}
      </p>
    </div>
  );
};
