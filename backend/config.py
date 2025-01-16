from configuretron import env_base64_value, from_yaml
from dataclasses import dataclass
from os import environ


@dataclass
class Config:
    anthropic_api_key: str
    my_api_films_token: str
    opensubtitles_api_key: str
    opensubtitles_username: str
    opensubtitles_password: str
    youtube_api_key: str
    youtube_network_device: str | None


use_encryption = environ.get("CONFIG_PRIVATE_KEY", "") != ""

config: Config = from_yaml(
    Config,
    "/api/config.yml",
    private_key=env_base64_value("CONFIG_PRIVATE_KEY") if use_encryption else None,
    decrypt=use_encryption,
    env=environ.get("ENV", "development"),
)
