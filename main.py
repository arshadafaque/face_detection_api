from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.database import Base, engine
from src.api_router.routers import router as api_router
from src.api_router.service import initialize_face_model
from sqlalchemy import text


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Server Start")
    initialize_face_model()
    with engine.connect() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
        conn.commit()
    Base.metadata.create_all(bind=engine)
    yield
    print("Shutting down...")

app = FastAPI(title="Face Recognition API", lifespan=lifespan,tags=["Face Detect"])

app.include_router(api_router)


