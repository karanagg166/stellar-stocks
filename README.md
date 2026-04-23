# 🚀 JarNox Stock Intelligence Dashboard

A full-stack financial data platform built as an internship assignment for JarNox.

## 🏗️ Architecture

- **Frontend**: Next.js 15 (App Router), TypeScript, Tailwind CSS v3, shadcn/ui, Plotly.js
- **Backend**: FastAPI (Python), SQLModel, Pandas, yfinance
- **Database**: PostgreSQL
- **Containerization**: Docker Compose

## ✨ Features

- **Automated Data Pipeline**: Scrapes 1-year historical OHLCV data for 10 NSE stocks via `yfinance` and calculates advanced metrics (7-day MA, 52-week High/Low, Volatility Score).
- **REST API**: Fully documented FastAPI backend with auto-generated Swagger UI.
- **Interactive Dashboard**: Real-time market overview, top gainers/losers, and beautifully styled interactive Plotly charts.
- **Comparative Analysis**: Compare normalized percentage returns of two assets side-by-side and view their statistical Pearson correlation.

## 🛠️ Setup Instructions (Docker)

Ensure you have Docker and Docker Compose installed.

1. Clone the repository and navigate to the root directory.
2. Run the following command to build and start all services:
   ```bash
   docker-compose up --build -d
   ```
3. The stack will automatically:
   - Start the PostgreSQL database
   - Run the Python seed script to fetch and process stock data
   - Start the FastAPI backend
   - Start the Next.js frontend

### 🌐 Access URLs

- **Frontend Dashboard**: [http://localhost:3000](http://localhost:3000)
- **Backend API Docs (Swagger)**: [http://localhost:8000/docs](http://localhost:8000/docs)

## 📊 Analytics & Creativity

### Custom Metric: Volatility Score
The pipeline calculates a unique **Volatility Score** for each stock. This is computed as the annualized 20-day rolling standard deviation of daily returns. It helps quickly identify how risky or volatile an asset is currently trading.

### Comparative Correlation
The `/compare` endpoint calculates the **Pearson Correlation Coefficient** between the daily returns of two selected stocks over a specified period. This is visualized on the frontend to help determine if two stocks move together or independently.

---
*Built with ❤️ for the JarNox Engineering Team.*
