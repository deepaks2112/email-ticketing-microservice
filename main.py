from fastapi import FastAPI
from api.apis import router
import uvicorn
from tools.logger import logger

logger.info("Starting the application...")

app = FastAPI()


@app.get("/")
async def home():
    return {
        "description": "Welcome to ticket-generation-service API!"
    }

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=5000)
