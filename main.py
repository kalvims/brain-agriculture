from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routers import router
from app.core.logger import logger
from app.db.init_db import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Servidor iniciado com sucesso!")
    yield
    logger.info("Servidor encerrado.")


init_db()

app = FastAPI(lifespan=lifespan)

app.include_router(router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
