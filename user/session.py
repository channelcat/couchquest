from config import config
from dataclasses import dataclass
from fastapi import Cookie, Response
import jwt
from .models import User
from datetime import datetime, timedelta, timezone
from typing import Annotated


@dataclass
class Session:
    user_id: int
    expires: datetime


class AuthenticatedUser(User):
    is_authenticated = True


class CurrentUser(User):
    pass


async def create_session(user: User, response: Response):
    expires = datetime.now(timezone.utc) + timedelta(days=7)
    token = jwt.encode(
        {"user_id": user.id, "exp": expires},
        config.jwt_secret,
        algorithm="HS256",
    )
    response.set_cookie(
        key="token",
        value=token,
        expires=expires,
        httponly=True,
        path="/",
    )
    user.last_login_at = datetime.now(timezone.utc)
    await user.save()


def destroy_session(response: Response):
    response.set_cookie(
        key="token",
        value="",
        path="/",
        expires=datetime(1990, 1, 1, tzinfo=timezone.utc),
    )


def get_session(token: Annotated[str | None, Cookie()] = None) -> Session | None:
    if not token:
        return None
    try:
        token_data = jwt.decode(token, config.jwt_secret, algorithms=["HS256"])
        return Session(
            user_id=token_data["user_id"],
            expires=datetime.fromtimestamp(token_data["exp"], tz=timezone.utc),
        )
    except:
        return None
