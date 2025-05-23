from pydantic import BaseModel
from datetime import date

class PriceCreate(BaseModel):
    product: str
    region: str
    date: date
    price: float

class PriceOut(PriceCreate):
    id: int
    model_config = {"from_attributes": True}
    
class AvgPriceOut(BaseModel):
    region: str
    month: str
    avg_price: float