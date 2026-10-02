from fastapi import FastAPI

from app.database import Base
from app.database import engine

from app.routers.users import router as users_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="User API",
    version="1.0.0"
)

app.include_router(users_router)