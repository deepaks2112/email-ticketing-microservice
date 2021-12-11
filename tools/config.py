from pydantic import BaseSettings

class Constants:
    TICKET_RECORD_COLLECTION = "tickets"

class Settings(BaseSettings):
    MONGO_URL: str
    AES_KEY: str
    DB_NAME: str


config = Settings()

