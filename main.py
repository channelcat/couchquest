from coloco import create_app
from config import config

app = create_app(
    name="couchquest",
    # database_url=f"postgres://{config.database_user}:{config.database_password}@{config.database_host}:5432/{config.database_name}",
    database_url="sqlite://db.sqlite3",
)
