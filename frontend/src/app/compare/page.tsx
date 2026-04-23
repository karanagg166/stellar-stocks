import { api } from "@/lib/api";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ArrowLeftRight } from "lucide-react";
import StockChart from "@/components/StockChart"; // We'll adapt or create a specific compare chart if needed
import PlotlyChart from "@/components/PlotlyChart";
export default async function ComparePage({
  searchParams,
}: {
  searchParams: Promise<{ s1?: string; s2?: string }>;
}) {
  const { s1, s2 } = await searchParams;
  
  try {
    const allCompanies = await api.getCompanies();
    
    // Default to first two companies if none selected
    const symbol1 = s1 || allCompanies.companies[0]?.symbol || "RELIANCE.NS";
    const symbol2 = s2 || allCompanies.companies[1]?.symbol || "TCS.NS";

    const compareData = await api.compareStocks(symbol1, symbol2, 90);

    const dates = compareData.symbol1_data.map(d => d.date);
    
    // Normalize prices to percentage change from start of period for fair comparison
    const normalize = (data: any[]) => {
      if (!data.length) return [];
      const base = data[0].close;
      return data.map(d => ((d.close - base) / base) * 100);
    };

    const norm1 = normalize(compareData.symbol1_data);
    const norm2 = normalize(compareData.symbol2_data);

    return (
      <div className="p-8 space-y-8 max-w-6xl mx-auto">
        <div>
          <h1 className="text-3xl font-bold tracking-tight flex items-center gap-2">
            <ArrowLeftRight className="w-8 h-8 text-primary" />
            Compare Stocks
          </h1>
          <p className="text-muted-foreground mt-2">
            Compare 90-day normalized performance and correlation between two assets.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <Card className="border-blue-500/20 bg-blue-500/5">
            <CardHeader>
              <CardTitle className="text-blue-400">Asset 1: {compareData.symbol1_name}</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-xl font-bold font-mono">
                {compareData.symbol1.replace('.NS', '')}
              </div>
            </CardContent>
          </Card>

          <Card className="border-orange-500/20 bg-orange-500/5">
            <CardHeader>
              <CardTitle className="text-orange-400">Asset 2: {compareData.symbol2_name}</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-xl font-bold font-mono">
                {compareData.symbol2.replace('.NS', '')}
              </div>
            </CardContent>
          </Card>
        </div>

        <Card>
          <CardHeader>
            <CardTitle>90-Day Normalized Return (%)</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="w-full h-[450px]">
              <PlotlyChart
                data={[
                  {
                    x: dates,
                    y: norm1,
                    type: "scatter",
                    mode: "lines",
                    name: compareData.symbol1_name,
                    line: { color: "#3b82f6", width: 2 }, // blue-500
                  },
                  {
                    x: dates,
                    y: norm2,
                    type: "scatter",
                    mode: "lines",
                    name: compareData.symbol2_name,
                    line: { color: "#f97316", width: 2 }, // orange-500
                  },
                ]}
                layout={{
                  autosize: true,
                  margin: { t: 20, r: 20, l: 40, b: 40 },
                  paper_bgcolor: "transparent",
                  plot_bgcolor: "transparent",
                  font: { color: "#8b8fa3" },
                  xaxis: {
                    gridcolor: "rgba(255,255,255,0.1)",
                    zerolinecolor: "rgba(255,255,255,0.1)",
                  },
                  yaxis: {
                    title: "% Return",
                    gridcolor: "rgba(255,255,255,0.1)",
                    zerolinecolor: "rgba(255,255,255,0.4)",
                    ticksuffix: "%",
                  },
                  legend: { orientation: "h", y: -0.2 },
                }}
                useResizeHandler
                className="w-full h-full"
              />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Statistical Correlation</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex flex-col items-center justify-center py-6">
              <div className="text-5xl font-bold text-primary mb-2">
                {compareData.correlation !== null ? compareData.correlation.toFixed(3) : 'N/A'}
              </div>
              <p className="text-muted-foreground max-w-md text-center">
                Pearson correlation coefficient of daily returns over the last 90 days. 
                Values close to 1 indicate strong positive correlation, while values close to -1 indicate strong inverse correlation.
              </p>
            </div>
          </CardContent>
        </Card>
      </div>
    );
  } catch (e) {
    console.error("Failed to load comparison data:", e);
    return (
      <div className="p-8 space-y-4">
        <h1 className="text-2xl font-bold text-red-600">Failed to load comparison data</h1>
        <p className="text-muted-foreground">The server might be offline or the symbols might be invalid. Please check your backend connection.</p>
      </div>
    );
  }
}
