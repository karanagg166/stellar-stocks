from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import create_db_and_tables
from app.routers import companies, stock_data, summary, compare, top_movers


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle — create tables."""
    create_db_and_tables()
    yield


app = FastAPI(
    title=settings.APP_TITLE,
    version=settings.APP_VERSION,
    description=settings.APP_DESCRIPTION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS — allow frontend origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(companies.router, tags=["Companies"])
app.include_router(stock_data.router, tags=["Stock Data"])
app.include_router(summary.router, tags=["Summary"])
app.include_router(compare.router, tags=["Compare"])
app.include_router(top_movers.router, tags=["Top Movers"])


@app.get("/", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": settings.APP_TITLE}
