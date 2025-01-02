from datetime import date
from pydantic import BaseModel
from typing import Literal


class Episode(BaseModel):
    number: int
    title: str
    id: str | int
    imdb_id: int


class Season(BaseModel):
    number: int
    episodes: list[Episode]


class SearchResult(BaseModel):
    title: str
    release_year: int
    service: str
    id: str | int
    imdb_id: int
    image_url: str
    url: str
    type: Literal["movie", "series"]
    seasons: list[Season]
    release_date: date | None = None


class SearchResults(BaseModel):
    results: list[SearchResult]


class ActionRequest(BaseModel):
    action: str
    amount: int
    theme: str


class GenerateRequest(BaseModel):
    id: str | int
    service: str
    imdb_id: int
    desired_actions: list[ActionRequest]
    parent_imdb_id: int | None = None


class GeneratedSuggestion(BaseModel):
    suggestion: str
    estimated_amount: int | None = None


class GeneratedGame(BaseModel):
    name: str
    instructions: str
    theme: str
    estimated_amount: int


class GeneratedAction(BaseModel):
    action: str
    games: list[GeneratedGame]


class GeneratedGames(BaseModel):
    explanation: str
    suggestions: list[GeneratedSuggestion]
    actions: list[GeneratedAction]
