import pandas as pd
from datetime import datetime
from .database import SessionLocal
from .crud import create_price
from .schemas import PriceCreate

def load_data_from_excel(path: str):
    df = pd.read_excel(path)
    df = df.rename(columns={
        "Województwo": "region",
        "Data": "date",
        "Cena": "price",
        "Produkt": "product"
    })
    db = SessionLocal()
    for _, row in df.iterrows():
        entry = PriceCreate(
            product=row['product'],
            region=row['region'],
            date=pd.to_datetime(row['date']).date(),
            price=row['price']
        )
        create_price(db, entry)
    db.close()
