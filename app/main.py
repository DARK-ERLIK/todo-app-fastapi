from fastapi import FastAPI
from .database import engine, Base
from .routers import auth, todos

app = FastAPI(
    title="ToDo App",
    description="A simple ToDo application with authentication",
    version="1.0.0"
)

# Подключаем роутеры
app.include_router(auth.router)
app.include_router(todos.router)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the ToDo App!"}
