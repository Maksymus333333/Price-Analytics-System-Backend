from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from . import crud, schemas, models
from .database import engine, SessionLocal
from .data_loader import load_data_from_excel
import os
from pathlib import Path

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

EXCEL_PATH = "data/prices_poland_extended_1000.xlsx"
TIMESTAMP_FILE = "data/.last_imported.txt"

@app.on_event("startup")
def startup_event():
    try:
        excel_mtime = os.path.getmtime(EXCEL_PATH)
        excel_mtime_str = str(excel_mtime)

        Path("data").mkdir(parents=True, exist_ok=True)

        if os.path.exists(TIMESTAMP_FILE):
            with open(TIMESTAMP_FILE, "r") as f:
                last_loaded = f.read().strip()
        else:
            last_loaded = ""

        if excel_mtime_str != last_loaded:
            print("[INFO] Excel file changed. Reloading data...")
            db = SessionLocal()
            db.query(models.ProductPrice).delete()
            db.commit()
            db.close()

            load_data_from_excel(EXCEL_PATH)

            with open(TIMESTAMP_FILE, "w") as f:
                f.write(excel_mtime_str)

            print("[INFO] Data reloaded.")
        else:
            print("[INFO] Excel not changed. Skipping reload.")
    except Exception as e:
        print(f"[ERROR] during Excel check: {e}")

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

    return [
        {
            "product": r[0],
            "region": r[1],
            "date": r[2],
            "price": round(r[3], 2)
        }
        for r in results
    ]

@app.get("/debug-count")
def debug_count(db: Session = Depends(get_db)):
    return {"count": db.query(models.ProductPrice).count()}
