"use client";

import dynamic from "next/dynamic";
import { StockData } from "@/lib/types";

// Dynamically import plotly to avoid SSR issues
const Plot = dynamic(() => import("react-plotly.js"), { ssr: false });

interface StockChartProps {
  data: StockData[];
  symbol: string;
}

export default function StockChart({ data, symbol }: StockChartProps) {
  const dates = data.map((d) => d.date);
  const closes = data.map((d) => d.close);
  const ma7 = data.map((d) => d.moving_avg_7d);

  return (
    <div className="w-full h-[400px] border rounded-lg p-4 bg-card">
      <Plot
        data={[
          {
            x: dates,
            y: closes,
            type: "scatter",
            mode: "lines",
            name: "Close Price",
            line: { color: "#00d68f", width: 2 },
          },
          {
            x: dates,
            y: ma7,
            type: "scatter",
            mode: "lines",
            name: "7D Moving Avg",
            line: { color: "#8b8fa3", width: 1, dash: "dot" },
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
            gridcolor: "rgba(255,255,255,0.1)",
            zerolinecolor: "rgba(255,255,255,0.1)",
          },
          legend: { orientation: "h", y: -0.2 },
        }}
        useResizeHandler
        className="w-full h-full"
      />
    </div>
  );
}
