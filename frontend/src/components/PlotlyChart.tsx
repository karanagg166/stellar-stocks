"use client";
import dynamic from "next/dynamic";

const Plot = dynamic(() => import("react-plotly.js"), { ssr: false });

export default function PlotlyChart(props: any) {
  return <Plot {...props} />;
}
