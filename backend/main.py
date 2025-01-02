import asyncio
from data import GenerateRequest, GeneratedGame, GeneratedGames, SearchResult
import logging
import myapifilms
import opensubtitles
from service import api, UserError


def format_srt(srt: bytes) -> str:
    srt_txt = srt.decode("utf-8")
    blocks = srt_txt.split("\n\n")

    output = []
    nl = "\n"
    for block in blocks:
        lines = block.split(nl)
        start_time, end_time = lines[1].split(" --> ")
        output.append(f"{start_time[:-4]}: {nl.join(lines[2:])}")
    return "\n\n".join(output)


async def none():
    return None


@api.get("/search")
async def media_search(query: str) -> list[SearchResult]:
    # TODO: support multiple languages
    results = [*await opensubtitles.search(query, filter_language="en")]

    return results


@api.post("/generate")
async def generate(request: GenerateRequest) -> GeneratedGames:
    # TODO: support multiple languages

    subtitles, summary, parent_summary = await asyncio.gather(
        opensubtitles.download_best_subtitles(request.id, language="en"),
        myapifilms.get_imdb_summary(request.imdb_id),
        (
            myapifilms.get_imdb_summary(request.parent_imdb_id)
            if request.parent_imdb_id
            else none()
        ),
    )

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
