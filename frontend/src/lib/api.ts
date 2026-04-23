import {
  CompanyListResponse,
  StockDataListResponse,
  Summary,
  TopMovers,
  CompareResponse,
} from "./types";

// Server-side (SSR) uses the Docker internal URL; browser uses the public URL
const API_BASE =
  typeof window === "undefined"
    ? process.env.API_URL || process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"
    : process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function fetchJson<T>(endpoint: string): Promise<T> {
  const res = await fetch(`${API_BASE}${endpoint}`, { cache: "no-store" });
  if (!res.ok) {
    throw new Error(`Failed to fetch API: ${endpoint} - ${res.statusText}`);
  }
  return res.json() as Promise<T>;
}

export const api = {
  getCompanies: () => fetchJson<CompanyListResponse>("/companies"),
  
  getStockData: (symbol: string, days: number = 30) => 
    fetchJson<StockDataListResponse>(`/data/${symbol}?days=${days}`),
  
  getSummary: (symbol: string) => fetchJson<Summary>(`/summary/${symbol}`),
  
  getTopMovers: () => fetchJson<TopMovers>("/top-movers"),
  
  compareStocks: (symbol1: string, symbol2: string, days: number = 30) =>
    fetchJson<CompareResponse>(`/compare?symbol1=${symbol1}&symbol2=${symbol2}&days=${days}`),
};
