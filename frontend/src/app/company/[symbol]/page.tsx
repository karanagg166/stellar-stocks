import { api } from "@/lib/api";
import StockChart from "@/components/StockChart";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

export const dynamic = "force-dynamic";

export default async function CompanyPage({
  params,
}: {
  params: Promise<{ symbol: string }>;
}) {
  const { symbol } = await params;
  
  try {
    // Fetch data in parallel
    const [stockData, summary] = await Promise.all([
      api.getStockData(symbol, 90), // Get 90 days for chart
      api.getSummary(symbol),
    ]);

    const latest = stockData.data[stockData.data.length - 1];
    const isPositive = latest.daily_return >= 0;

    return (
      <div className="p-8 space-y-8 max-w-6xl mx-auto">
        {/* Header */}
        <div className="flex flex-col md:flex-row justify-between items-start md:items-end gap-4">
          <div>
            <div className="flex items-center gap-3 mb-2">
              <h1 className="text-4xl font-bold tracking-tight">{summary.symbol.replace('.NS', '')}</h1>
              <Badge variant="secondary" className="text-sm">{summary.sector}</Badge>
            </div>
            <p className="text-muted-foreground text-lg">{summary.name}</p>
          </div>
          
          <div className="text-right">
            <div className="text-4xl font-bold font-mono">₹{summary.current_price.toFixed(2)}</div>
            <div className={`text-lg font-medium ${isPositive ? 'text-green-500' : 'text-red-500'}`}>
              {isPositive ? '+' : ''}{latest.daily_return.toFixed(2)}% Today
            </div>
          </div>
        </div>

        {/* Chart */}
        <div>
          <h2 className="text-xl font-semibold mb-4">Price History (90 Days)</h2>
          <StockChart data={stockData.data} symbol={summary.symbol} />
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">52-Week High</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-green-400">₹{summary.high_52w.toFixed(2)}</div>
            </CardContent>
          </Card>
          
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">52-Week Low</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-red-400">₹{summary.low_52w.toFixed(2)}</div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">Avg Close</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">₹{summary.avg_close.toFixed(2)}</div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">Volatility Score</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-yellow-500">
                {summary.volatility_score ? summary.volatility_score.toFixed(3) : 'N/A'}
              </div>
              <p className="text-xs text-muted-foreground mt-1">Annualized (20d std)</p>
            </CardContent>
          </Card>
        </div>
      </div>
    );
  } catch (e) {
    console.error("Failed to load company data:", e);
    return (
      <div className="p-8 space-y-4">
        <h1 className="text-2xl font-bold text-red-600">Failed to load data for {symbol}</h1>
        <p className="text-muted-foreground">The server might be offline or the symbol might be invalid. Please check your backend connection.</p>
      </div>
    );
  }
}
