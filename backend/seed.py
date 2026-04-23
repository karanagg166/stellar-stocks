"""
Seed Script — Fetches stock data from Yahoo Finance, cleans it,
adds calculated metrics, and loads it into PostgreSQL via SQLModel.

Usage (inside Docker):
    python seed.py
"""

import math
from datetime import datetime
from sqlmodel import Session, select

from app.database import engine, create_db_and_tables
from app.models import Company, StockData
from app.services.data_service import COMPANIES, fetch_and_prepare


def seed():
    """Fetch, transform, and load stock data for all companies."""
    # Ensure tables are created
    create_db_and_tables()

    print("=" * 60)
    print("🚀 Stock Data Seeder")
    print(f"   Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"   Companies: {len(COMPANIES)}")
    print("=" * 60)

    with Session(engine) as session:
        for symbol, info in COMPANIES.items():
            print(f"\n📊 Processing {symbol} ({info['name']})...")

            # Upsert company record
            company = session.exec(select(Company).where(Company.symbol == symbol)).first()
            if not company:
                company = Company(symbol=symbol, name=info["name"], sector=info["sector"])
                session.add(company)
                session.commit()
                session.refresh(company)
                print(f"   ✅ Created company record: id={company.id}")
            else:
                company.name = info["name"]
                company.sector = info["sector"]
                session.add(company)
                session.commit()
                print(f"   ✅ Updated company record: id={company.id}")

            # Fetch and prepare data
            df = fetch_and_prepare(symbol)
            if df.empty:
                print(f"   ⚠️  No data fetched, skipping...")
                continue

            print(f"   📈 Fetched {len(df)} records")

            # Delete existing stock data for this company (fresh seed)
            existing_records = session.exec(
                select(StockData).where(StockData.company_id == company.id)
            ).all()
            for r in existing_records:
                session.delete(r)
            session.commit()
            print(f"   🗑️  Cleared {len(existing_records)} old records")

            # Bulk insert new data
            inserted = 0
            stock_objects = []
            for _, row in df.iterrows():
                # Safely handle NaN values — convert to None
                def safe_float(val):
                    if val is None or (isinstance(val, float) and math.isnan(val)):
                        return None
                    return float(val)

                stock_objects.append(StockData(
                    company_id=company.id,
                    date=datetime.combine(row["date"], datetime.min.time()).date(),
                    open=float(row["open"]),
                    high=float(row["high"]),
                    low=float(row["low"]),
                    close=float(row["close"]),
                    volume=int(row["volume"]),
                    daily_return=float(row["daily_return"]),
                    moving_avg_7d=safe_float(row.get("moving_avg_7d")),
                    high_52w=float(row["high_52w"]),
                    low_52w=float(row["low_52w"]),
                    volatility_score=safe_float(row.get("volatility_score")),
                ))
                inserted += 1

            session.add_all(stock_objects)
            session.commit()
            print(f"   ✅ Inserted {inserted} records")

        # Print summary
        total_companies = len(session.exec(select(Company)).all())
        total_records = len(session.exec(select(StockData)).all())
        print("\n" + "=" * 60)
        print(f"🏁 Seeding complete!")
        print(f"   Companies: {total_companies}")
        print(f"   Total stock records: {total_records}")
        print("=" * 60)


if __name__ == "__main__":
    seed()
