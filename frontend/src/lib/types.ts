export interface Company {
  id: number;
  symbol: string;
  name: string;
  sector: string;
}

export interface CompanyListResponse {
  count: number;
  companies: Company[];
}

export interface StockData {
  date: string;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
  daily_return: number;
  moving_avg_7d: number | null;
  high_52w: number;
  low_52w: number;
  volatility_score: number | null;
}

export interface StockDataListResponse {
  symbol: string;
  name: string;
  days: number;
  data: StockData[];
}

export interface Summary {
  symbol: string;
  name: string;
  sector: string;
  current_price: number;
  high_52w: number;
  low_52w: number;
  avg_close: number;
  total_return_1y: number;
  volatility_score: number | null;
  volume_avg: number;
}

export interface MoverItem {
  symbol: string;
  name: string;
  daily_return: number;
  close: number;
}

export interface TopMovers {
  gainers: MoverItem[];
  losers: MoverItem[];
}

export interface CompareResponse {
  symbol1: string;
  symbol1_name: string;
  symbol2: string;
  symbol2_name: string;
  symbol1_data: StockData[];
  symbol2_data: StockData[];
  correlation: number | null;
}
