import asyncio
from logging.config import fileConfig
from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context
from app.database import Base
from app.config import settings

# Настройка логирования Alembic
config = context.config
fileConfig(config.config_file_name)

config.set_main_option("sqlalchemy.url", settings.SQLALCHEMY_DATABASE_URL)

# Установите URL вашей БД
DATABASE_URL = settings.SQLALCHEMY_DATABASE_URL
target_metadata = Base.metadata


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata, compare_type=True)
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    connectable = create_async_engine(DATABASE_URL, future=True)

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()

asyncio.run(run_migrations_online())
