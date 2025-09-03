from fastapi import FastAPI
from app.controllers import order_controller
from app.db.session import engine
from app.db.base import init_db

app = FastAPI(title="Orders API")

app.include_router(order_controller.router, prefix="/api", tags=["Orders"])

# Хук запуска при старте приложения
@app.on_event("startup")
async def on_startup():
    await init_db(engine)
