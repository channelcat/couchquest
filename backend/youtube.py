from config import config
from data import SearchResult
from datetime import datetime
from pyyoutube import Client
import re
from util import run_sync_in_async
from youtube_transcript_api import YouTubeTranscriptApi

client = Client(api_key=config.youtube_api_key)


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
    videos = await run_sync_in_async(client.videos.list, video_id=video_id)
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
    videos = await run_sync_in_async(client.videos.list, video_id=video_id)
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


async def get_video_subtitles(video_id):
    transcript = await run_sync_in_async(YouTubeTranscriptApi.get_transcript, video_id)
    return "\n\n".join(f"[{t['start']}s] {t['text']}" for t in transcript)
