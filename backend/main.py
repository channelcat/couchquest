from data import GenerateRequest, GeneratedGame, GeneratedGames, SearchResult
from service import api, UserError
import opensubtitles


@api.get("/search")
async def media_search(query: str) -> list[SearchResult]:
    # TODO: support multiple languages
    results = [*await opensubtitles.search(query, filter_language="en")]

    return results


@api.post("/generate")
async def generate(request: GenerateRequest) -> GeneratedGames:
    # TODO: support multiple languages

    # Fetch subtitles
    subtitles = await opensubtitles.download_best_subtitles(request.id, language="en")
    with open("/tmp/subtitles.srt", "wb") as f:
        f.write(subtitles)

    # Fetch synopsis

    # Generate games
    # Return results

    raise Exception("Not implemented")

    return GeneratedGames(
        explanation="Explanation",
        suggestions=["Suggestion 1", "Suggestion 2"],
        games=[
            GeneratedGame(
                name="Game 1",
                theme="Theme 1",
                instructions="Instructions",
                estimated_drinks=10,
                estimated_finishes=2,
            ),
            GeneratedGame(
                name="Game 2",
                theme="Theme 2",
                instructions="Instructions",
                estimated_drinks=10,
                estimated_finishes=2,
            ),
        ],
    )
