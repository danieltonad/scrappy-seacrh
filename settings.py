import os
from dotenv import load_dotenv

load_dotenv(override=True)


class Settings:
    DB_PATH = os.getenv("DB_PATH")
    
    
settings = Settings()