import asyncio
from .data import (
    GeneratedAction,
    GeneratedGame,
    GeneratedGames,
    GenerateRequest,
    GeneratedSuggestion,
)
from fastapi import APIRouter
import logging
from vendor import anthropic, myapifilms, opensubtitles, youtube

router = APIRouter()


async def none():
    return None


@router.post("/generate")
async def game_generate(request: GenerateRequest) -> GeneratedGames:
    # TODO: support multiple languages

    prompt_resources = []

    if request.service == "youtube":
        (title, channel, description), subtitles = await asyncio.gather(
            youtube.get_video_details(request.id),
            youtube.get_video_subtitles(request.id),
        )
        prompt_resources.append(f"<title>{title}</title>")
        prompt_resources.append(f"<channel>{channel}</channel>")
        prompt_resources.append(f"<description>{description}</description>")
        prompt_resources.append(f"<transcript>{subtitles}</transcript>")
        feature_type = "youtube video"

    elif request.service == "opensubtitles":
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

        if is_show:
            prompt_resources.append(f"<show summary>{parent_summary}</show summary>")
            prompt_resources.append(f"<episode summary>{summary}</episode summary>")
        else:
            prompt_resources.append(f"<summary>{summary}</summary>")
        prompt_resources.append(f"<transcript>{subtitles}</transcript>")

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
    {"\n".join(action_prompts)}

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
            *prompt_resources,
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
