import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.logging import setup_logging
from app.routers.commodities import router as commodities_router

# ── Bootstrap logging before anything else ────────────────────────────────────
setup_logging()
logger = logging.getLogger(__name__)

# ── FastAPI app ───────────────────────────────────────────────────────────────
app = FastAPI(
    title="Commodity Data API",
    description=(
        "Production-grade REST API exposing commodity profiles, trade summaries, "
        "and news feeds sourced from PostgreSQL views."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# ── CORS ──────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(commodities_router)


# ── Health check ──────────────────────────────────────────────────────────────
@app.get("/health", tags=["Health"], summary="Service health check")
async def health():
    return {"status": "ok", "service": "commodity-data-api"}


# ── Global exception handlers ─────────────────────────────────────────────────
@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    logger.warning("404 Not Found: %s", request.url)
    return JSONResponse(
        status_code=404,
        content={"detail": "Resource not found", "path": str(request.url)},
    )


@app.exception_handler(500)
async def internal_error_handler(request: Request, exc):
    logger.exception("500 Internal Server Error: %s", request.url)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "path": str(request.url)},
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled exception on %s: %s", request.url, str(exc))
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc), "path": str(request.url)},
    )


# ── Startup / shutdown events ─────────────────────────────────────────────────
@app.on_event("startup")
async def on_startup():
    logger.info("Commodity Data API started — CORS origins: %s", settings.cors_origins_list)


@app.on_event("shutdown")
async def on_shutdown():
    logger.info("Commodity Data API shutting down")
