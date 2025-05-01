import asyncio
from app.database import create_db_and_tables

asyncio.run(create_db_and_tables())
