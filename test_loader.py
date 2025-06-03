from app.data_loader import load_data_from_excel
from app.database import SessionLocal
from app import models
import os

if __name__ == "__main__":
    print(">>> Шлях до бази:", os.path.abspath("app/../prices.db"))
    print(">>> Існує база?", os.path.exists("app/../prices.db"))

    # Створимо таблиці, якщо не існують
    models.Base.metadata.create_all(bind=SessionLocal().get_bind())

    load_data_from_excel("data/symulowane_ceny_produktow.xlsx")
    print("Завантаження завершено.")