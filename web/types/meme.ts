export interface MemeResult {
  id: number;
  filename: string;
  url: string;
  score: number;
  captions: string[];
}

export interface SearchResponse {
  query: string;
  results: MemeResult[];
}

