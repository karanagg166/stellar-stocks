"use client";
import dynamic from "next/dynamic";

const Plot = dynamic(() => import("react-plotly.js"), { ssr: false });

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export default function PlotlyChart(props: any) {
  return <Plot {...props} />;
}
