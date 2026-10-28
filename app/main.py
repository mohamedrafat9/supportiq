from fastapi import FastAPI
from app.api.routes.tickets import router as tickets_router

app = FastAPI(title="SupportIQ API")
app.include_router(tickets_router)

@app.get("/health")
def health_check():
    return {"status":"ok"}

