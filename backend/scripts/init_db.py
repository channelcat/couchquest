import sys
import time
import asyncio
from tortoise import Tortoise, connections
from backend.config import config

async def wait_for_db():
    max_retries = 30
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            await Tortoise.init(
                db_url=config.database_url,
                modules={'models': ['models']}
            )
            await Tortoise.generate_schemas()
            await Tortoise.close_connections()
            print("Successfully connected to the database and initialized schemas!")
            return True
        except Exception as e:
            print(f"Database not ready yet... (Attempt {retry_count + 1}/{max_retries})")
            retry_count += 1
            await asyncio.sleep(2)
    
    print("Failed to connect to the database after maximum retries")
    return False

success = asyncio.run(wait_for_db())
if not success:
    sys.exit(1)