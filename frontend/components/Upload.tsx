// components/Upload.tsx
import React, { useCallback, useRef, useState } from "react";
import { uploadPDF, ApiError } from "../services/api";

interface UploadProps {
  onUploadSuccess: (docId: string) => void;
  onUploadError: (message: string) => void;
  isUploading: boolean;
  setIsUploading: (v: boolean) => void;
  docId: string | null;
}

export const Upload: React.FC<UploadProps> = ({
  onUploadSuccess,
  onUploadError,
  isUploading,
  setIsUploading,
  docId,
}) => {
  const inputRef = useRef<HTMLInputElement>(null);
  const [dragOver, setDragOver] = useState(false);
  const [fileName, setFileName] = useState<string | null>(null);

  const handleFile = useCallback(
    async (file: File) => {
      if (file.type !== "application/pdf") {
        onUploadError("Only PDF files are supported.");
        return;
      }

      setFileName(file.name);
      setIsUploading(true);

      try {
        const response = await uploadPDF(file);
        onUploadSuccess(response.doc_id);
      } catch (err) {
        const msg =
          err instanceof ApiError
            ? err.message
            : "Upload failed. Please try again.";
        onUploadError(msg);
        setFileName(null);
      } finally {
        setIsUploading(false);
      }
    },
    [onUploadSuccess, onUploadError, setIsUploading]
  );

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) handleFile(file);
    // reset so same file can be re-uploaded
    e.target.value = "";
  };

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setDragOver(false);
    const file = e.dataTransfer.files?.[0];
    if (file) handleFile(file);
  };

  return (
    <div className="upload-wrapper">
      <div
        className={`upload-zone ${dragOver ? "drag-over" : ""} ${docId ? "uploaded" : ""} ${isUploading ? "uploading" : ""}`}
        onClick={() => !isUploading && inputRef.current?.click()}
        onDragOver={(e) => {
          e.preventDefault();
          setDragOver(true);
        }}
        onDragLeave={() => setDragOver(false)}
        onDrop={handleDrop}
        role="button"
        tabIndex={0}
        onKeyDown={(e) => e.key === "Enter" && inputRef.current?.click()}
        aria-label="Upload PDF"
      >
        <input
          ref={inputRef}
          type="file"
          accept="application/pdf"
          onChange={handleInputChange}
          style={{ display: "none" }}
        />

        {isUploading ? (
          <div className="upload-state">
            <div className="spinner" />
            <span className="upload-label">Indexing document…</span>
          </div>
        ) : docId ? (
          <div className="upload-state success">
            <span className="upload-icon">✓</span>
            <span className="upload-label">{fileName}</span>
            <span className="upload-sub">Click to replace</span>
          </div>
        ) : (
          <div className="upload-state">
            <span className="upload-icon pdf-icon">
              <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
                <rect
                  x="4"
                  y="2"
                  width="18"
                  height="24"
                  rx="2"
                  stroke="currentColor"
                  strokeWidth="1.5"
                  fill="none"
                />
                <path
                  d="M10 2v6H4"
                  stroke="currentColor"
                  strokeWidth="1.5"
                  strokeLinejoin="round"
                />
                <path
                  d="M18 16H8M14 20H8M16 12H8"
                  stroke="currentColor"
                  strokeWidth="1.5"
                  strokeLinecap="round"
                />
                <circle cx="24" cy="24" r="7" fill="var(--accent)" />
                <path
                  d="M24 21v6M21 24l3-3 3 3"
                  stroke="white"
                  strokeWidth="1.5"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
              </svg>
            </span>
            <span className="upload-label">Drop your PDF here</span>
            <span className="upload-sub">or click to browse</span>
          </div>
        )}
      </div>
    </div>
  );
};
