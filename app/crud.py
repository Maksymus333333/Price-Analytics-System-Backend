from sqlalchemy.orm import Session
from . import models, schemas

def create_price(db: Session, price: schemas.PriceCreate):
    db_price = models.ProductPrice(**price.dict())
    db.add(db_price)
    db.commit()
    db.refresh(db_price)
    return db_price

def get_all_prices(db: Session):
    return db.query(models.ProductPrice).all()
