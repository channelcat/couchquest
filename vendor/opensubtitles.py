from config import config
from httpx import AsyncClient, Response
from json.decoder import JSONDecodeError
from os import environ
import logging
from api.data import Episode, Season, SearchResult

TOKEN = None
BASE_URL = "https://api.opensubtitles.com/api/v1"


async def request(method, uri, use_token=True, **kwargs):
    headers = {
        "User-Agent": "httpx",
        "Api-Key": config.opensubtitles_api_key,
        "Content-Type": "application/json",
    }
    if use_token:
        headers["Authorization"] = f"Bearer {await get_token()}"
    if "headers" in kwargs:
        headers.update(kwargs["headers"])
        del kwargs["headers"]
    if "timeout" not in kwargs:
        kwargs["timeout"] = 30
    if "follow_redirects" not in kwargs:
        kwargs["follow_redirects"] = True

    async with AsyncClient() as client:
        response: Response = await getattr(client, method.lower())(
            f"{BASE_URL}{uri}", headers=headers, **kwargs
        )
        try:
            result = response.json()
        except JSONDecodeError:
            raise LookupError(
                f"OpenSubtitles error: {uri} - {response.status_code} - {response.text}"
            )

        # Request Error
        if not 200 <= response.status_code < 300:
            error = (
                f"OpenSubtitles error: {response.status_code} {result.get('message')}"
            )
            logging.error(error)
            raise Exception(error)

        # API Error
        if "status" in result and result["status"] != 200:
            error = f"OpenSubtitles error: {result.get('status')} {','.join(result.get('errors', []))}"
            logging.error(error)
            raise Exception(error)

        return result


async def get_token():
    global TOKEN
    if not TOKEN:
        logging.info("Logging in to OpenSubtitles...")
        response = await request(
            "POST",
            "/login",
            use_token=False,
            json={
                "username": config.opensubtitles_username,
                "password": config.opensubtitles_password,
            },
            follow_redirects=False,
        )
        TOKEN = response["token"]
        logging.info("Successfully logged in to OpenSubtitles")
    return TOKEN


def parse_image_url(url: str) -> str:
    if url.startswith("/"):
        return f"https://www.opensubtitles.com{url}"
    return url


async def search(query: str, filter_language: str = None) -> list[dict]:
    response = await request(
        "GET", f"/features", params={"query": query}, use_token=False
    )

    results = [
        result["attributes"]
        for result in response["data"]
        if (
            result["attributes"]["subtitles_counts"].get(filter_language, 0) > 0
            if filter_language
            else True
        )
    ]

    return [
        SearchResult(
            title=result["title"],
            release_year=(
                int(result["year"])
                if type(result["year"]) is int
                or type(result["year"]) is str
                and result["year"].isnumeric()
                else None
            ),
            service="opensubtitles",
            id=result["feature_id"],
            imdb_id=result["imdb_id"],
            image_url=parse_image_url(result["img_url"]),
            url=result["url"],
            type="series" if result.get("seasons") else "movie",
            seasons=[
                Season(
                    number=season["season_number"],
                    episodes=[
                        Episode(
                            number=episode["episode_number"],
                            title=episode["title"],
                            id=episode["feature_id"],
                            imdb_id=episode["feature_imdb_id"],
                        )
                        for episode in season["episodes"]
                    ],
                )
                for season in (result.get("seasons") or [])
            ],
        )
        for result in results
    ]


async def download_subtitles(file_id: int) -> bytes:
    response = await request(
        "POST",
        f"/download",
        json={"file_id": file_id},
    )
    logging.info(f"Downloading subtitles {response['file_name']}...")
    logging.info(
        f"{response['requests']} sent, {response['remaining']} remaining until {response['reset_time_utc']}"
    )

    file_url = response["link"]

    async with AsyncClient() as client:
        response = await client.get(file_url)
        return response.content


async def download_best_subtitles(feature_id: int, language: str) -> bytes:
    response = await request(
        "GET",
        f"/subtitles",
        params={
            "languages": language,
            "order_by": "download_count",
            "order_direction": "desc",
            "id": feature_id,
        },
    )

    # TODO: find out why frieren episode 18 is missing subtitles
    if not response["data"]:
        raise LookupError("No subtitles found")

    sorted_results = sorted(
        response["data"],
        key=lambda s: (
            s["attributes"]["hearing_impaired"] or False,
            s["attributes"]["from_trusted"] or False,
            s["attributes"]["download_count"] or 0,
        ),
        reverse=True,
    )
    file_id = sorted_results[0]["attributes"]["files"][0]["file_id"]

    return await download_subtitles(file_id)
