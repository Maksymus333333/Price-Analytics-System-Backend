from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from . import crud, schemas, models
from .database import engine, SessionLocal
from sqlalchemy import func

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/prices", response_model=list[schemas.PriceOut])
def read_prices(db: Session = Depends(get_db)):
    return crud.get_all_prices(db)

@app.get("/avg-prices")
def avg_prices_by_region_and_month(db: Session = Depends(get_db)):
    results = db.query(
        models.ProductPrice.product,
        models.ProductPrice.region,
        func.strftime("%Y-%m", models.ProductPrice.date).label("date"),
        func.avg(models.ProductPrice.price).label("price")
    ).group_by(models.ProductPrice.product, models.ProductPrice.region, "date").all()

    # перетворимо в список словників, щоб фронт зрозумів
    return [
        {
            "product": r[0],
            "region": r[1],
            "date": r[2],
            "price": round(r[3], 2)
        }
        for r in results
    ]
