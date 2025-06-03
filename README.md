# 🥦 Food Price Analytics Backend

A FastAPI-based backend for loading, storing, and analyzing food price data across Polish regions. This project reads Excel files with product prices and exposes clean API endpoints for querying and aggregating the data.

---

## 📦 Features

- 📁 Load food prices from Excel files (with regional, product, and date information)
- 🗂️ Store them in a SQLite database via SQLAlchemy ORM
- 🌐 Serve prices via a RESTful API built with FastAPI
- 📊 Return monthly average prices per region/product
- 🧪 Debug endpoints for quick checks

---

## 🚀 Tech Stack

- **FastAPI** – RESTful API
- **Pandas** – Excel data parsing
- **SQLAlchemy** – ORM with SQLite backend
- **Pydantic** – Request/response validation
- **Uvicorn** – ASGI server

---

## ⚙️ Setup Instructions

### 1. Clone the repository

### 2. Create virtual environment and install dependencies

python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

pip install -r requirements.txt

### 3. Load Excel data into the database

python test_loader.py

### 4. Running the API Server

uvicorn app.main:app --reload
