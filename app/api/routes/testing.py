from fastapi import FastAPI , Response ,HTTPException
from pydantic import BaseModel, EmailStr
from fastapi.responses import JSONResponse

app = FastAPI()
class Product(BaseModel):
    name: str
    price: float
    description: str
    email: EmailStr

@app.post("/path/{product_id}")
async def get_product(product_id: int,
                      category:str,
                      data:Product)->Response:
    return JSONResponse(content={"product_id": product_id, "category": category, "data": data.model_dump()})