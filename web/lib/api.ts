import type { SearchResponse } from "@/types/meme";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

async function parseResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const body = await response.json().catch(() => null);
    throw new Error(body?.detail ?? "请求失败，请稍后再试");
  }
  return response.json() as Promise<T>;
}

export async function searchMemes(query: string): Promise<SearchResponse> {
  const response = await fetch(`${API_URL}/api/search`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query, limit: 6 }),
  });
  return parseResponse<SearchResponse>(response);
}

export async function recordClick(memeId: number, query: string): Promise<void> {
  await fetch(`${API_URL}/api/clicks`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ meme_id: memeId, query }),
  });
}

export async function uploadMeme(file: File): Promise<void> {
  const data = new FormData();
  data.append("file", file);
  const response = await fetch(`${API_URL}/api/memes/upload`, {
    method: "POST",
    body: data,
  });
  await parseResponse(response);
}

