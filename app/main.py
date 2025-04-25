from fastapi import FastAPI
from app.routers import weather
import uvicorn

app = FastAPI()
app.include_router(weather.router)

if __name__ == "__main__":
    uvicorn.run(app, port=8000)