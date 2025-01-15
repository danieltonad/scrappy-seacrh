import os
from dotenv import load_dotenv

load_dotenv(override=True)


class Settings:
    BINANCE_UID = int(os.getenv("binance_uid"))
    MEXC_UID = int(os.getenv("bybit_uid"))
    BYBIT_UID = int(os.getenv("mexc_uid"))
    DB_PATH = os.getenv("DB_PATH")
    
    
settings = Settings()