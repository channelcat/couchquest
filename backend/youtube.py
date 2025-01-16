from config import config
from data import SearchResult
from datetime import datetime
import httpx
import json
from pyyoutube import Client
import re
from util import run_sync_in_async
from youtube_transcript_api import YouTubeTranscriptApi

client = None


def get_client():
    global client
    if not client:
        client = Client(api_key=config.youtube_api_key)
    return client


def extract_video_id(url):
    """
    Extract YouTube video ID from various forms of YouTube URLs.
    Returns None if the URL is invalid or not a YouTube URL.

    Supports:
    - youtube.com/watch?v=VIDEO_ID
    - youtu.be/VIDEO_ID
    - youtube.com/embed/VIDEO_ID
    - youtube.com/v/VIDEO_ID
    - youtube.com/shorts/VIDEO_ID

    Args:
        url (str): The YouTube URL or string to parse

    Returns:
        str or None: The video ID if found, None otherwise
    """
    if not isinstance(url, str):
        return None

    # Regular expressions for different YouTube URL formats
    patterns = [
        r'(?:youtube\.com/(?:[^/]+/.+/|(?:v|e(?:mbed)?)/|.*[?&]v=)|youtu\.be/)([^"&?/ ]{11})',
        r'youtube\.com/shorts/([^"&?/ ]{11})',
    ]

    # Try each pattern
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)

    return None


async def search_video(video_id):
    videos = await run_sync_in_async(get_client().videos.list, video_id=video_id)
    if type(videos) is dict:
        raise Exception(f"Error fetching video {video_id}: {videos}")
    if not videos.items:
        raise Exception(f"No video found for {video_id}")

    return [
        SearchResult(
            title=video.snippet.title,
            release_year=datetime.fromisoformat(video.snippet.publishedAt).year,
            service="youtube",
            id=video.id,
            imdb_id=None,
            image_url=(
                video.snippet.thumbnails.default.url
                if hasattr(video.snippet.thumbnails, "default")
                else None
            ),
            url=f"https://www.youtube.com/watch?v={video.id}",
            type="video",
        )
        for video in videos.items
    ]


async def get_video_details(video_id):
    videos = await run_sync_in_async(get_client().videos.list, video_id=video_id)
    if type(videos) is dict:
        raise Exception(f"Error fetching video {video_id}: {videos}")
    if not videos.items:
        raise Exception(f"No video found for {video_id}")
    video = videos.items[0]
    return (
        video.snippet.title,
        video.snippet.channelTitle,
        video.snippet.description,
    )


# API-based (requires OAuth2)


async def get_video_subtitles_official(video_id):
    client = get_client()
    captions = await run_sync_in_async(client.captions.list, video_id=video_id)
    if type(captions) is dict:
        raise Exception(f"Error fetching captions for {video_id}: {captions}")

    caption_id = None
    for caption in captions.items:
        if caption.snippet.language == "en":
            caption_id = caption.id
            break
    else:
        raise Exception(f"No captions found for {video_id}")
    return await run_sync_in_async(client.captions.download, caption_id=caption_id)


# Janky Extraction


async def get_video_subtitles(video_id):
    try:
        transcript = await run_sync_in_async(
            YouTubeTranscriptApi.get_transcript,
            video_id,
            proxies=["http://138.68.60.8:8080"],
        )
        return "\n\n".join(f"[{t['start']}s] {t['text']}" for t in transcript)
    except Exception as e:
        try:
            return await get_video_generated_subtitles(video_id)
        except Exception as e:
            raise Exception(f"Failed to get video subtitles")


async def get_video_generated_subtitles(video_id):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://www.youtube.com/watch?v={video_id}")
        html_content = response.text
        # TODO: Add support for other languages
        track_url = extract_caption_track_url(html_content, language="en")
        if not track_url:
            raise LookupError("No caption track found")
        response = await client.get(track_url)
        return response.text


def extract_caption_track_url(html_content, language="en"):
    """
    Extract caption tracks data from YouTube HTML content.

    Args:
        html_content (str): The HTML content from a YouTube page

    Returns:
        list: List of caption track objects, or empty list if none found

    Example caption track object:
    {
        'baseUrl': 'https://www.youtube.com/api/timedtext?...',
        'name': {'simpleText': 'English (auto-generated)'},
        'vssId': 'a.en',
        'languageCode': 'en',
        'kind': 'asr',
        'isTranslatable': True
    }
    """

    # Find the ytInitialPlayerResponse object in the script
    pattern = r"var ytInitialPlayerResponse = ({.*?});"
    match = re.search(pattern, html_content, re.DOTALL)

    if not match:
        return []

    try:
        # Parse the JSON content
        player_response = json.loads(match.group(1))

        # Navigate to captions data
        captions = player_response.get("captions", {})
        player_captions = captions.get("playerCaptionsTracklistRenderer", {})
        caption_tracks = player_captions.get("captionTracks", [])

        for track in caption_tracks:
            if track.get("languageCode") == language:
                return track.get("baseUrl")

    except (json.JSONDecodeError, AttributeError, KeyError):
        pass

    return None
