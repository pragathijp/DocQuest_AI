// ============================================================
// services/api.ts — ALL fetch/API logic lives here ONLY
// Components must NEVER call fetch() directly.
// ============================================================

export interface UploadResponse {
  doc_id: string;
  status: "indexed" | "error";
}

export interface HistoryMessage {
  role: "user" | "assistant";
  content: string;
}

export interface QueryRequest {
  query: string;
  doc_id: string;
  history: HistoryMessage[];
}

export interface SourcePreview {
  preview: string;
}

export interface QueryResponse {
  answer: string;
  sources: SourcePreview[];
  confidence: number;
}

export class ApiError extends Error {
  constructor(
    message: string,
    public statusCode?: number
  ) {
    super(message);
    this.name = "ApiError";
  }
}

const BASE_URL =
  process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export async function uploadPDF(
  file: File
): Promise<UploadResponse> {
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(`${BASE_URL}/upload`, {
    method: "POST",
    body: formData,
  });

  if (!res.ok) {
    const text = await res.text().catch(() => "");

    let friendlyMessage =
      "Upload failed. Please try again.";

    if (text.includes("no extractable text")) {
      friendlyMessage =
        "This PDF has no readable text. Please upload a text-based PDF, not a scanned image.";
    } else if (text.includes("Pipeline aborted")) {
      friendlyMessage =
        "Could not process this PDF. Please try a different file.";
    } else if (text.includes("bad file")) {
      friendlyMessage =
        "Invalid file. Please upload a valid PDF.";
    }

    throw new ApiError(friendlyMessage, res.status);
  }

  return res.json() as Promise<UploadResponse>;
}

export async function queryDocument(
  request: QueryRequest
): Promise<QueryResponse> {
  const res = await fetch(`${BASE_URL}/query`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(request),
  });

  if (!res.ok) {
    const text = await res.text().catch(
      () => "Unknown error"
    );

    throw new ApiError(
      `Query failed: ${text}`,
      res.status
    );
  }

  return res.json() as Promise<QueryResponse>;
}