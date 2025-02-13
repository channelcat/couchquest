from config import config

TORTOISE_ORM = {
    "connections": {
        "default": f"postgres://{config.database_user}:{config.database_password}@{config.database_host}:5432/{config.database_name}"
    },
    "apps": {
        "models": {
            "models": [
                "models.user",
                "aerich.models",
            ],
            "default_connection": "default",
        },
    },
}
