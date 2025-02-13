from api import game, media, user, auth
from contextlib import asynccontextmanager
from database import TORTOISE_ORM
from fastapi import FastAPI
from service import api
from service.lifespan import register_lifespan
from tortoise import Tortoise


@asynccontextmanager
async def load_database(app: FastAPI):
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()
    yield
    await Tortoise.close_connections()


register_lifespan(load_database)

api.include_router(game.router, prefix="/game", tags=["game"])
api.include_router(media.router, prefix="/media", tags=["media"])
api.include_router(auth.router, prefix="/auth", tags=["auth"])
api.include_router(user.router, prefix="/user", tags=["user"])
