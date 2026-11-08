from fastapi import FastAPI
from app.api.routes.tickets import router as tickets_router
from app.api.routes.document import router as document_router

app = FastAPI(title="SupportIQ API")
app.include_router(tickets_router)
app.include_router(document_router)

@app.get("/health")
def health_check():
    return {"status":"ok"}


@app.get("/")
def root():
    return {"root":"hey this the root page "}