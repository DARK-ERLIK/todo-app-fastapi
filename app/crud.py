from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from . import models, schemas

async def get_user(db: AsyncSession, username: str):
    result = await db.execute(select(models.User).where(models.User.username == username))
    return result.scalars().first()

async def get_todo(db: AsyncSession, todo_id: int, user_id: int):
    result = await db.execute(
        select(models.ToDo)
        .where(models.ToDo.id == todo_id)
        .where(models.ToDo.owner_id == user_id)
    )
    return result.scalars().first()

async def get_todos(db: AsyncSession, user_id: int, skip: int = 0, limit: int = 100):
    result = await db.execute(
        select(models.ToDo)
        .where(models.ToDo.owner_id == user_id)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()
