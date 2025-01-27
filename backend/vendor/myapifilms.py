from config import config
from httpx import AsyncClient, Response
from os import environ
import logging


BASE_URL = "https://www.myapifilms.com"


async def request(method, uri, **kwargs):
    # TODO: support multiple languages
    params = {"token": config.my_api_films_token, "format": "json", "language": "en-us"}
    if kwargs.get("params"):
        params.update(kwargs["params"])
        del kwargs["params"]
    async with AsyncClient() as client:
        response: Response = await getattr(client, method.lower())(
            f"{BASE_URL}{uri}", params=params, **kwargs
        )
        result = response.json()

        # Request Error
        if not 200 <= response.status_code < 300:
            error = f"MyAPIFilms error: {response.status_code} {result.get('message')}"
            logging.error(error)
            raise Exception(error)

        return result


async def get_imdb_summary(imdb_id: int) -> str:
    response = await request(
        "GET",
        f"/imdb/idIMDB",
        params={
            "idIMDB": f"tt{str(imdb_id).zfill(7)}",
            "aka": 0,
            "business": 0,
            "seasons": 0,
            "seasonYear": 0,
            "technical": 0,
            "trailers": 0,
            "movieTrivia": 0,
            "awards": 0,
            "moviePhotos": 0,
            "movieVideos": 0,
            "actors": 0,
            "biography": 0,
            "uniqueName": 0,
            "filmography": 0,
            "bornDied": 0,
            "starSign": 0,
            "actorActress": 1,
            "actorTrivia": 0,
            "similarMovies": 0,
            "goofs": 0,
            "keyword": 0,
            "quotes": 0,
            "fullSize": 0,
            "companyCredits": 0,
            "filmingLocations": 0,
            # "directors": 1,
            # "writers": 2,
        },
    )
    if not response.get("data") or not response["data"].get("movies"):
        raise LookupError("No summary found")

    return response["data"]["movies"][0]["simplePlot"]
