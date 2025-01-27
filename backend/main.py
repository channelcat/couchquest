from service import api
from api import auth, game, media, user

api.include_router(game.router, prefix="/game", tags=["game"])
api.include_router(media.router, prefix="/media", tags=["media"])
api.include_router(auth.router, prefix="/auth", tags=["auth"])
api.include_router(user.router, prefix="/user", tags=["user"])
