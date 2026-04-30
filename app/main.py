import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import ResponseValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.config import settings
from app.core.logging import setup_logging
from app.routers.commodities import router as commodities_router
from app.routers.admin import router as admin_router

setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Commodity Data API",
    description="""
Production-grade REST API exposing commodity profiles, trade summaries, and news feeds sourced from PostgreSQL views.

## Routers

### Commodities — Read
Endpoints for querying commodity data from PostgreSQL views:
- **Profiles** — full commodity details including definition, uses, major producers, trade record count, and news count
- **Trade Summary** — aggregated trade data filterable by commodity name and year
- **Latest News** — paginated news feed ordered by publication date
- **High-Impact News** — filtered view of high-impact news, optionally scoped to a commodity

### Admin — Write
CRUD endpoints for managing the underlying commodity data:
- **Commodities** — create and update commodity records
- **News** — add and update news articles linked to a commodity
- **Trade** — add and update trade records linked to a commodity

## Notes
- All list endpoints return a `{ total_count, items }` paginated envelope
- Write endpoints validate that the referenced `commodity_id` exists before inserting
- CORS is configured via `CORS_ORIGINS` in `.env`; all `localhost` ports are allowed by default
- Logs are written to `logs/app.log`

## Start the server
```
source .venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8002
```
""",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# ── CORS must be the FIRST middleware added ───────────────────────────────────
# Using allow_origins=["*"] is safe here because credentials are not sent.
# To restrict, set CORS_ORIGINS in .env and swap ["*"] for settings.cors_origins_list
_cors_origins = settings.cors_origins_list
logger.info("Registering CORS origins: %s", _cors_origins)

app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins,
    allow_origin_regex=r"http://localhost:\d+",  # catch any localhost port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


# ── Catch-all error middleware — runs INSIDE CORS so headers are always set ───
class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except Exception as exc:
            logger.exception("Unhandled error on %s: %s", request.url, exc)
            return JSONResponse(
                status_code=500,
                content={"detail": str(exc), "path": str(request.url)},
            )


app.add_middleware(ErrorHandlerMiddleware)

# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(commodities_router)
app.include_router(admin_router)


# ── Health check ──────────────────────────────────────────────────────────────
@app.get("/health", tags=["Health"], summary="Service health check")
async def health():
    return {"status": "ok", "service": "commodity-data-api"}


# ── Exception handlers (for HTTPException / 404 etc.) ────────────────────────
@app.exception_handler(ResponseValidationError)
async def response_validation_error_handler(request: Request, exc: ResponseValidationError):
    logger.error("Response validation error on %s: %s", request.url, exc.errors())
    return JSONResponse(
        status_code=500,
        content={"detail": "Response serialization error", "errors": exc.errors()},
    )


@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    logger.warning("404: %s", request.url)
    return JSONResponse(
        status_code=404,
        content={"detail": "Resource not found", "path": str(request.url)},
    )


@app.exception_handler(500)
async def internal_error_handler(request: Request, exc):
    logger.error("500: %s", request.url)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "path": str(request.url)},
    )


@app.on_event("startup")
async def on_startup():
    logger.info("Commodity Data API started — port 8002")
    logger.info("CORS origins (%d): %s", len(_cors_origins), _cors_origins)


@app.on_event("shutdown")
async def on_shutdown():
    logger.info("Commodity Data API shutting down")
