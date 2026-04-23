import Link from "next/link";
import { api } from "@/lib/api";
import { BarChart3, Home, ArrowLeftRight } from "lucide-react";

export default async function Sidebar() {
  const data = await api.getCompanies();

  return (
    <div className="w-64 flex flex-col border-r bg-background min-h-screen">
      <div className="p-6 border-b">
        <h1 className="text-xl font-bold flex items-center gap-2">
          <BarChart3 className="w-6 h-6 text-primary" />
          JarNox Intel
        </h1>
      </div>
      
      <div className="p-4 flex flex-col gap-2 border-b">
        <Link 
          href="/" 
          className="flex items-center gap-2 px-3 py-2 rounded-md hover:bg-accent text-sm font-medium transition-colors"
        >
          <Home className="w-4 h-4" />
          Dashboard Overview
        </Link>
        <Link 
          href="/compare" 
          className="flex items-center gap-2 px-3 py-2 rounded-md hover:bg-accent text-sm font-medium transition-colors"
        >
          <ArrowLeftRight className="w-4 h-4" />
          Compare Stocks
        </Link>
      </div>

      <div className="flex-1 overflow-y-auto p-4">
        <h2 className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-3 px-3">
          Companies
        </h2>
        <div className="flex flex-col gap-1">
          {data.companies.map((company) => (
            <Link
              key={company.symbol}
              href={`/company/${company.symbol}`}
              className="flex flex-col px-3 py-2 rounded-md hover:bg-accent transition-colors"
            >
              <span className="font-semibold text-sm">{company.symbol.replace('.NS', '')}</span>
              <span className="text-xs text-muted-foreground truncate">{company.name}</span>
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
}
