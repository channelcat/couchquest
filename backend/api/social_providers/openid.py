from dataclasses import dataclass


@dataclass
class OpenID:
    id: str
    email: str
    display_name: str
    picture: str
    provider: str
