import logging
from contextlib import asynccontextmanager

from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import ALLOWED_ORIGINS
from app.jobs.weather_refresh_job import refresh_all_locations
from app.routers import auth, forecast

logging.basicConfig(level=logging.INFO)

scheduler = BackgroundScheduler()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # TEMPORARY for testing: fires every 15 seconds so you can watch it work.
    # Change to hours=3 once confirmed, before committing.
    scheduler.add_job(refresh_all_locations, "interval", seconds=30,id="weather_refresh")
    scheduler.start()
    yield
    scheduler.shutdown()


app = FastAPI(title="EcoSync API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(forecast.router)


@app.get("/health")
def health():
    return {"status": "ok"}