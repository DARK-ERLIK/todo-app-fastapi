from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from ..database import get_db
from ..models import ToDo, User
from ..schemas import ToDoCreate, ToDoOut, ToDoUpdate
from .auth import get_current_user

router = APIRouter(
    prefix="/todos",
    tags=["todos"]
)


@router.post("/", response_model=ToDoOut, status_code=status.HTTP_201_CREATED)
async def create_todo(
        todo: ToDoCreate,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    db_todo = ToDo(**todo.dict(), owner_id=current_user.id)
    db.add(db_todo)
    await db.commit()
    await db.refresh(db_todo)
    return db_todo


@router.get("/", response_model=List[ToDoOut])
async def read_todos(
        skip: int = 0,
        limit: int = 100,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(ToDo)
        .where(ToDo.owner_id == current_user.id)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


@router.get("/{todo_id}", response_model=ToDoOut)
async def read_todo(
        todo_id: int,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(ToDo)
        .where(ToDo.id == todo_id)
        .where(ToDo.owner_id == current_user.id)
    )
    todo = result.scalars().first()
    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    return todo


@router.put("/{todo_id}", response_model=ToDoOut)
async def update_todo(
        todo_id: int,
        todo: ToDoUpdate,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(ToDo)
        .where(ToDo.id == todo_id)
        .where(ToDo.owner_id == current_user.id)
    )
    db_todo = result.scalars().first()
    if db_todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

    update_data = todo.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_todo, field, value)

    db.add(db_todo)
    await db.commit()
    await db.refresh(db_todo)
    return db_todo


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
        todo_id: int,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(ToDo)
        .where(ToDo.id == todo_id)
        .where(ToDo.owner_id == current_user.id)
    )
    db_todo = result.scalars().first()
    if db_todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

    await db.delete(db_todo)
    await db.commit()
    return None
