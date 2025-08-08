from fastapi import FastAPI
from src.models.db import Base, engine
from src.api.hero_api import router as hero_router
import uvicorn

app = FastAPI()
app.include_router(hero_router)

#выполнение один раз при старте
@app.on_event("startup")
async def startup():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
