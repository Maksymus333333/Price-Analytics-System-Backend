from sqlalchemy import Column, Integer, String, Float, Date
from .database import Base

class ProductPrice(Base):
    __tablename__ = "product_prices"
    id = Column(Integer, primary_key=True, index=True)
    product = Column(String, index=True)
    region = Column(String, index=True)
    date = Column(Date)
    price = Column(Float)
