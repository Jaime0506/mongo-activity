from fastapi import FastAPI
from config.database import connect_to_mongo, close_mongo_connection
from contextlib import asynccontextmanager
from routes.router_car import router as router_car
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    # === startup ===
    await connect_to_mongo()
    try:
        yield
    finally:
        # === shutdown ===
        await close_mongo_connection()

app = FastAPI(lifespan=lifespan)

app.include_router(router_car)


@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)