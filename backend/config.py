from configuretron import env_base64_value, from_yaml
from dataclasses import dataclass


@dataclass
class Config:
    anthropic_api_key: str
    my_api_films_token: str
    opensubtitles_api_key: str
    opensubtitles_username: str
    opensubtitles_password: str
    youtube_api_key: str


config: Config = from_yaml(
    Config, "/api/config.yml", private_key=env_base64_value("CONFIG_PRIVATE_KEY")
)
