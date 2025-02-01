from config import config
from fastapi import APIRouter
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2AuthorizationCodeBearer
from google.oauth2 import id_token
from google.auth.transport import requests
import os

router = APIRouter()

# OAuth2 configuration for Google
oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="https://accounts.google.com/o/oauth2/v2/auth",
    tokenUrl="https://oauth2.googleapis.com/token"
)

GOOGLE_CLIENT_ID = config.google_client_id
GOOGLE_CLIENT_SECRET = config.google_client_secret

@router.post("/google")
async def google_auth(token: str = Depends(oauth2_scheme)):
    try:
        # Verify the token with Google
        idinfo = id_token.verify_oauth2_token(
            token, 
            requests.Request(),
            GOOGLE_CLIENT_ID
        )

        # Check if the token is issued by Google
        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid issuer"
            )

        # Extract user information
        user_info = {
            "email": idinfo['email'],
            "name": idinfo['name'],
            "picture": idinfo.get('picture'),
            "google_id": idinfo['sub']
        }

        return user_info

    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

@router.get("/google/url")
async def get_google_auth_url():
    return {
        "url": f"https://accounts.google.com/o/oauth2/v2/auth?"
        f"client_id={GOOGLE_CLIENT_ID}&"
        "response_type=code&"
        "scope=openid email profile&"
        "access_type=offline&"
        f"redirect_uri={config.google_redirect_uri}"
    }
