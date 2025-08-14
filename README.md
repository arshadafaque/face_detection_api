# Face Detection API

A FastAPI-based face detection and recognition API using InsightFace (ArcFace) for embedding extraction and face matching.

## Features
- Upload an image and get detected faces with bounding boxes
- Compare uploaded face against stored embeddings
- Store user face embeddings in PostgreSQL
- Dockerized setup with `docker-compose`

## Tech Stack
- **FastAPI** (API framework)
- **InsightFace / ArcFace** (face embeddings)
- **PostgreSQL** (storage)
- **SQLAlchemy** (ORM)
- **Docker & Docker Compose** (containerization)

---

## Installation

### 1️⃣ Clone the repository
```bash
git clone [https://github.com/your-username/face_detection_api.git](https://github.com/arshadafaque/face_detection_api.git)
cd face_detection_api
