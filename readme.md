# SupportIQ

An AI-powered customer support platform with RAG-based answer generation, semantic retrieval, 
and observability.

## Stack

- **Backend** — Python / FastAPI
- **Database** — PostgreSQL 16
- **Vector Store** — Qdrant
- **Cache / Queue** — Redis 7
- **Observability** — Arize Phoenix (LLM tracing)

## Getting Started

```bash
# 1. Copy env file and fill in values
cp .env.example .env

# 2. Start infrastructure
docker compose up -d

# 3. Install dependencies & run the app
pip install -r requirements.txt
uvicorn app.main:app --reload
```