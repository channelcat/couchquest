from .data import SearchResult
from fastapi import APIRouter
from vendor import opensubtitles, youtube
from service import api

router = APIRouter()


@router.get("/search")
async def media_search(query: str) -> list[SearchResult]:
    youtube_id = youtube.extract_video_id(query)
    if youtube_id:
        results = await youtube.search_video(youtube_id)
    else:
        # TODO: support multiple languages
        results = await opensubtitles.search(query, filter_language="en")

    return results
