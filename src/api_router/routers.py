from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database import SessionLocal
from src.database.models import FaceEmbedding
from .service import get_face_embedding
from sqlalchemy import select
import uuid

router = APIRouter(prefix="/api")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/add_face/")
async def add_face(name: str = Form(...), image: UploadFile = File(...), db: Session = Depends(get_db)):
    contents = await image.read()
    emb = get_face_embedding(contents)
    if emb is None:
        raise HTTPException(status_code=400, detail="No face detected in image")
    user_id = str(uuid.uuid4())
    face = FaceEmbedding(id=user_id, name=name, embedding=emb.tolist())
    db.add(face)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"DB error: {e}")
    return {"success": True, "id": face.id, "name": face.name}

@router.post("/match_face/")
async def match_face(image: UploadFile = File(...),  db: Session = Depends(get_db)):
    contents = await image.read()
    top_k: int = 1
    emb = get_face_embedding(contents)
    if emb is None:
        raise HTTPException(status_code=400, detail="No face detected in image")

    stmt = (
    select(
        FaceEmbedding.id,
        FaceEmbedding.name,
        (1 - FaceEmbedding.embedding.cosine_distance(emb)).label("similarity")
    )
    .order_by((1 - FaceEmbedding.embedding.cosine_distance(emb)).desc())  # Highest first
    .limit(top_k)
    )

    rows = db.execute(stmt).fetchall()
    if rows and rows[0].similarity >= 0.5:

        results = {
            "Message":"Matched",
            "Match":[ {"id": r.id, "name": r.name, "distance": float(r.similarity)} for r in rows]
        }
        return results
    else:
        return {
            "Message":"UnMatched",
            "Name":"No Face Found"
        }

