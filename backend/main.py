import anthropic
import asyncio
from data import (
    GeneratedAction,
    GeneratedGame,
    GeneratedGames,
    GenerateRequest,
    GeneratedSuggestion,
    SearchResult,
)
import logging
import myapifilms
import opensubtitles
from service import api, UserError

NEWLINE = "\n"


def format_srt(srt: bytes) -> str:
    srt_txt = srt.decode("utf-8")
    blocks = srt_txt.split("\n\n")

    output = []
    for block in blocks:
        lines = block.split(NEWLINE)
        start_time, end_time = lines[1].split(" --> ")
        output.append(f"{start_time[:-4]}: {NEWLINE.join(lines[2:])}")
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

    # Fetch subtitles, synopses
    subtitles, summary, parent_summary = await asyncio.gather(
        opensubtitles.download_best_subtitles(request.id, language="en"),
        myapifilms.get_imdb_summary(request.imdb_id),
        (
            myapifilms.get_imdb_summary(request.parent_imdb_id)
            if request.parent_imdb_id
            else none()
        ),
    )

    is_show = bool(request.parent_imdb_id)
    feature_type = "episode of a show" if is_show else "movie"

    # Assemble action prompts
    action_prompts = []
    for action in request.desired_actions:
        action_prompt = f"{action.action}, ideally {action.amount} times"
        if action.theme:
            action_prompt = f" - {action_prompt}, with a theme of {action.theme}"

        action_prompts.append(action_prompt)

    # Assemble prompt
    prompt = f"""
    You are a game master at a party creating a fun game to be played alongside a {feature_type} your partygoers are about to watch.
    
    Here are a list of actions they want to include in the game. Each action has a name, a number of times it should ideally be performed, and an optional theme.
    
    Actions:
    {NEWLINE.join(action_prompts)}

    Please generate 3-5 potential games per action, each with a name, instructions, and estimated amount of times it will be performed.  
    Also generate a list of suggestions for other actions or themes that could be fun to include in future games.
    
    Please return the results as valid JSON in the following format (all fields to be filled are written in <xml>):
    {{
        "explanation": <explanation of the games and actions as a string>,
        "suggestions": [
            {{
                "suggestion": <suggestion as a string>,
                "estimated_amount": <estimated amount of times the suggested action will be performed as an integer, or null if not applicable>
            }}
        ],
        "actions": [
            {{
                "action": <action name as a string>,
                "games": [
                    {{
                        "name": <a creative game name as a string>,
                        "instructions": <instructions of what is to be performed at what occurrence as a string>,
                        "theme": <theme of the game if applicable as a string>,
                        "estimated_amount": <estimated amount of times the action will be performed as an integer>
                    }}
                ]
            }}
        ]
    }}
    """

    logging.debug(f"Prompting claude: {prompt}")
    claude_response = await anthropic.claude_request_json(
        messages=[
            *(
                [
                    f"<show summary>{parent_summary}</show summary>",
                    f"<episode summary>{summary}</episode summary>",
                ]
                if is_show
                else [
                    f"<summary>{summary}</summary>",
                ]
            ),
            f"<transcript>{subtitles}</transcript>",
            prompt,
        ]
    )

    return GeneratedGames(
        explanation=claude_response.get("explanation"),
        suggestions=[
            GeneratedSuggestion(
                suggestion=suggestion.get("suggestion"),
                estimated_amount=suggestion.get("estimated_amount"),
            )
            for suggestion in claude_response.get("suggestions", [])
        ],
        actions=[
            GeneratedAction(
                action=action.get("action"),
                games=[
                    GeneratedGame(
                        name=game.get("name"),
                        instructions=game.get("instructions"),
                        theme=game.get("theme"),
                        estimated_amount=game.get("estimated_amount"),
                    )
                    for game in action.get("games", [])
                ],
            )
            for action in claude_response.get("actions", [])
        ],
    )
