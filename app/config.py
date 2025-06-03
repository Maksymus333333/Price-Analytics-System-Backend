# app/config.py
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "prices.db")
DATABASE_URL = f"sqlite:///{DB_PATH}"
