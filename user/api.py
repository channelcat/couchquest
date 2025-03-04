from coloco import api
from .providers import CurrentUser

from .models import User

@api
async def me(user: CurrentUser):
    return (
        {
            "authenticated": True,
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "picture": user.picture,
        }
        if user
        else {
            "autenticated": False,
            "id": None,
            "email": None,
            "name": "Guest",
            "picture": None,
        }
    )
