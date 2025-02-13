from httpx import AsyncClient
from .openid import OpenID
from time import time


async def user_from_google(client_id, token, allowed_drift=0):
    # Create an aiohttp session for async requests
    async with AsyncClient() as client:
        # Google's OAuth2 verification endpoint
        response = await client.get(
            "https://oauth2.googleapis.com/tokeninfo",
            params={"id_token": token},
        )
        if response.status_code != 200:
            raise ValueError("Invalid token")
        idinfo = response.json()
    if idinfo["aud"] != client_id:
        raise ValueError("Wrong client ID.")
    if idinfo["iss"] not in ["accounts.google.com", "https://accounts.google.com"]:
        raise ValueError("Wrong issuer.")

    now = int(time())
    if now < int(idinfo["iat"]) - allowed_drift:
        raise ValueError("Token used before issued")
    if now > int(idinfo["exp"]) + allowed_drift:
        raise ValueError("Token has expired")

    if not idinfo["email_verified"]:
        raise ValueError("Please verify your email with google.")

    return OpenID(
        id=idinfo["sub"],
        email=idinfo["email"],
        display_name=idinfo["name"],
        picture=idinfo["picture"],
        provider="google",
    )
