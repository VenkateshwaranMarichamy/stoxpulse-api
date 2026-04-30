# Commodity Data API

Production-grade REST API exposing commodity profiles, trade summaries, and news feeds sourced from PostgreSQL views.

Built with **FastAPI**, **SQLAlchemy (async)**, **asyncpg**, and **PostgreSQL**.

---

## Project Structure

```
stoxpulse-api/
├── app/
│   ├── main.py              # FastAPI app entry point
│   ├── database.py          # Async SQLAlchemy engine & session
│   ├── models.py            # SQLAlchemy ORM models (mapped to PG views)
│   ├── schemas.py           # Pydantic request/response schemas
│   ├── crud.py              # Database query functions
│   ├── routers/
│   │   ├── commodities.py   # Read endpoints (profiles, trade, news)
│   │   └── admin.py         # Write endpoints (CRUD for commodities, news, trade)
│   └── core/
│       ├── config.py        # Settings loaded from .env
│       └── logging.py       # Logging configuration
├── sql/
│   └── create_views.sql     # PostgreSQL view definitions
├── logs/
│   └── app.log              # Runtime log output
├── .env                     # Local environment variables (not committed)
├── .env.example             # Environment variable template
└── requirements.txt
```

---

## Setup

### 1. Create and activate virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment

```bash
cp .env.example .env
```

Edit `.env` with your PostgreSQL credentials:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=yourdb
DB_USER=youruser
DB_PASSWORD=yourpass

# Comma-separated list of allowed CORS origins
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

### 4. Start the server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8002
```

---

## API Endpoints

Interactive docs available at:
- Swagger UI: `http://localhost:8002/docs`
- ReDoc: `http://localhost:8002/redoc`

### Health

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Service health check |

### Commodities — Read

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/commodities/profiles` | List all commodity profiles (paginated) |
| GET | `/api/commodities/profiles/{profile_id}` | Get a single commodity profile by ID |
| GET | `/api/commodities/trade-summary` | Trade summaries — filter by `commodity` and/or `year` |
| GET | `/api/commodities/latest-news` | Latest commodity news feed — supports `limit` / `offset` |
| GET | `/api/commodities/high-impact-news` | High-impact news — filter by `commodity`, supports `limit` / `offset` |
| GET | `/api/commodities/list` | Simple list of all commodities (id, name, category) |

### Admin — Write

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/commodities/` | Add a new commodity |
| PATCH | `/api/commodities/{commodity_id}` | Update an existing commodity |
| POST | `/api/commodities/news` | Add a news article for a commodity |
| PATCH | `/api/commodities/news/{news_id}` | Update a news article |
| POST | `/api/commodities/trade` | Add a trade record for a commodity |
| PATCH | `/api/commodities/trade/{trade_id}` | Update a trade record |

---

## Query Parameters

### `GET /api/commodities/trade-summary`
| Param | Type | Description |
|-------|------|-------------|
| `commodity` | string | Case-insensitive partial match on commodity name |
| `year` | integer | Filter by year (1900–2100) |

### `GET /api/commodities/latest-news`
| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `limit` | integer | 50 | Max records to return (1–500) |
| `offset` | integer | 0 | Pagination offset |

### `GET /api/commodities/high-impact-news`
| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `commodity` | string | — | Case-insensitive partial match |
| `limit` | integer | 50 | Max records to return (1–500) |
| `offset` | integer | 0 | Pagination offset |

---

## Response Format

All list endpoints return a paginated envelope:

```json
{
  "total_count": 42,
  "items": [ ... ]
}
```

---

## CORS

Allowed origins are configured via `CORS_ORIGINS` in `.env` as a comma-separated list. All `localhost` ports are additionally allowed via regex. To add a production origin, append it to `CORS_ORIGINS`.

---

## Logging

Logs are written to `logs/app.log` and stdout. Log level and format are configured in `app/core/logging.py`.

---

## Requirements

- Python 3.11+
- PostgreSQL with the `commodities` schema and views defined in `sql/create_views.sql`
