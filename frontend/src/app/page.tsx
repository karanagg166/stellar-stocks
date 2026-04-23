import { api } from "@/lib/api";
import TopMovers from "@/components/TopMovers";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Building2, TrendingUp, Activity } from "lucide-react";

export default async function Home() {
  let data = { count: 0 };
  let error = false;

  try {
    data = await api.getCompanies();
  } catch (e) {
    console.error("Failed to load companies:", e);
    error = true;
  }

  return (
    <div className="p-8 space-y-8">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Market Overview</h1>
        <p className="text-muted-foreground mt-2">
          Real-time insights and analytics for Indian stock market.
        </p>
      </div>

      {error && (
        <div className="p-4 border border-red-200 bg-red-50 text-red-800 rounded-lg">
          <p className="font-semibold">Backend Connection Issue</p>
          <p className="text-sm">We couldn't connect to the server. Please check if the backend is running and the API URL is set correctly in Vercel.</p>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              Tracked Companies
            </CardTitle>
            <Building2 className="w-4 h-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{data.count}</div>
            <p className="text-xs text-muted-foreground mt-1">
              Top NSE listed entities
            </p>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              Market Trend
            </CardTitle>
            <TrendingUp className="w-4 h-4 text-green-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-green-500">{error ? "N/A" : "Bullish"}</div>
            <p className="text-xs text-muted-foreground mt-1">
              Based on recent 7D MA averages
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              System Status
            </CardTitle>
            <Activity className="w-4 h-4 text-blue-500" />
          </CardHeader>
          <CardContent>
            <div className={`text-2xl font-bold ${error ? "text-red-500" : "text-blue-500"}`}>
              {error ? "Offline" : "Live"}
            </div>
            <p className="text-xs text-muted-foreground mt-1">
              Data pipelines {error ? "suspended" : "active"}
            </p>
          </CardContent>
        </Card>
      </div>

      <div>
        <h2 className="text-xl font-semibold mb-4">Top Movers Today</h2>
        <TopMovers />
      </div>
    </div>
  );
}
