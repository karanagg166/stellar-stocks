import { api } from "@/lib/api";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ArrowUpRight, ArrowDownRight } from "lucide-react";
import Link from "next/link";

export default async function TopMovers() {
  const movers = await api.getTopMovers();

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      <Card>
        <CardHeader>
          <CardTitle className="text-lg flex items-center gap-2 text-green-500">
            <ArrowUpRight className="w-5 h-5" />
            Top Gainers
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {movers.gainers.map((stock) => (
              <div key={stock.symbol} className="flex items-center justify-between">
                <div className="flex flex-col">
                  <Link href={`/company/${stock.symbol}`} className="font-semibold hover:underline">
                    {stock.symbol.replace(".NS", "")}
                  </Link>
                  <span className="text-xs text-muted-foreground">{stock.name}</span>
                </div>
                <div className="flex flex-col items-end">
                  <span className="font-medium">₹{stock.close.toFixed(2)}</span>
                  <Badge variant="outline" className="text-green-500 bg-green-500/10 border-green-500/20">
                    +{stock.daily_return.toFixed(2)}%
                  </Badge>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="text-lg flex items-center gap-2 text-red-500">
            <ArrowDownRight className="w-5 h-5" />
            Top Losers
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {movers.losers.map((stock) => (
              <div key={stock.symbol} className="flex items-center justify-between">
                <div className="flex flex-col">
                  <Link href={`/company/${stock.symbol}`} className="font-semibold hover:underline">
                    {stock.symbol.replace(".NS", "")}
                  </Link>
                  <span className="text-xs text-muted-foreground">{stock.name}</span>
                </div>
                <div className="flex flex-col items-end">
                  <span className="font-medium">₹{stock.close.toFixed(2)}</span>
                  <Badge variant="outline" className="text-red-500 bg-red-500/10 border-red-500/20">
                    {stock.daily_return.toFixed(2)}%
                  </Badge>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
