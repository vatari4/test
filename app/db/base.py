from sqlalchemy.ext.asyncio import AsyncEngine
from app.db.models import Base

async def init_db(engine: AsyncEngine):     
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)




# Создает все таблицы в БД (если их ещё нет), используется только на этапе разработки!!! в проде лучше использовать миграции.