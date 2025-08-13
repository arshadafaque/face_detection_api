from sqlalchemy import Column, Integer, String
from pgvector.sqlalchemy import Vector
from . import Base

class FaceEmbedding(Base):
    __tablename__ = "face_embeddings"

    id = Column(String, primary_key=True, index=True) 
    name = Column(String, nullable=False)
    # store 512-dim ArcFace embedding
    embedding = Column(Vector(512), nullable=False)
