from coloco.exceptions import UserError
from fastapi import Depends
from .models import User
from .session import get_session, Session
from typing import Annotated


async def get_user_from_session(
    session: Session | None = Depends(get_session),
) -> User | None:
    if not session:
        return None
    return await User.get(id=session.user_id)


async def get_authenticated_user_from_session(
    session: Session | None = Depends(get_session),
) -> User:
    user = await get_user_from_session(session)
    if not user:
        raise UserError(
            "User session not found", code="session_not_found", status_code=401
        )
    return user


CurrentUser = Annotated[User, Depends(get_user_from_session)]
AuthenticatedUser = Annotated[User, Depends(get_authenticated_user_from_session)]
