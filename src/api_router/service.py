import numpy as np
from insightface.app import FaceAnalysis
import logging
import cv2

logging.basicConfig(
    level=logging.INFO,  
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("face_recognition.log"),
        logging.StreamHandler()  
    ]
)


apps = None

def initialize_face_model():
    global apps
    logging.info("Initializing FaceAnalysis model...")
    try:
        apps = FaceAnalysis(name='buffalo_l', providers=['CPUExecutionProvider'])
        apps.prepare(ctx_id=0,det_size=(640, 640))
        logging.info("Model initialized successfully.")
    except Exception as e:
        logging.error(f"Error initializing model: {e}")
        raise



def get_face_embedding(image_bytes):
    """Extracts face embedding from uploaded image bytes"""
    np_arr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    if img is None:
        logging.error("Uploaded file is not a valid image.")
        return None

    faces = apps.get(img)
    if not faces:
        logging.warning("No face detected in image.")
        return None
    return np.array(faces[0].normed_embedding)