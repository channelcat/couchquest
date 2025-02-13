from config import config
from fastapi import APIRouter, Request, Response
from models.user import User, ExternalAccount
from pydantic import BaseModel
from service.exceptions import UserError
from .session import create_session
from .social_providers.openid import OpenID
from .social_providers.google import user_from_google
from .user import user_me

router = APIRouter()


class GoogleSSO(BaseModel):
    token: str


class Providers(BaseModel):
    class Provider(BaseModel):
        client_id: str

    google: Provider


@router.get("/providers")
async def get_providers() -> Providers:
    return Providers(google=Providers.Provider(client_id=config.google_client_id))


@router.post("/google/callback")
async def google_oauth_callback(data: GoogleSSO, response: Response):
    user = await user_from_google(config.google_client_id, data.token, allowed_drift=10)
    return await login_user(user, response)


async def login_user(
    social_user: OpenID,
    response: Response,
):
    # Create External Account
    external_account, created = await ExternalAccount.get_or_create(
        external_id=social_user.id,
        provider=social_user.provider,
        defaults={
            "email": social_user.email,
            "name": social_user.display_name,
            "picture": social_user.picture,
        },
    )

    # Update External Account
    if (
        external_account.email != social_user.email
        or external_account.name != social_user.display_name
        or external_account.picture != social_user.picture
    ):
        external_account.email = social_user.email
        external_account.name = social_user.display_name
        external_account.picture = social_user.picture
        await external_account.save()

    # Create User
    if not external_account.user:
        user, created = await User.get_or_create(
            email=social_user.email,
            defaults={
                "name": social_user.display_name,
                "picture": social_user.picture,
            },
        )
        if not created:
            raise UserError("User already exists")

        external_account.user = user
        await external_account.save()
    else:
        user = await external_account.user

    await create_session(user, response)

    return await user_me(user)
