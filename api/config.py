import os

API_BASE_URL_WEATHER = "https://api.openweathermap.org/data/2.5/weather"
API_BASE_URL_FOREACH = "https://api.openweathermap.org/data/2.5/forecast"
API_KEY = "d5490057878699a6d9f20dcd6dd359f2"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")
DB_SQLLITE_HOST = f"sqlite:///{DB_PATH}"