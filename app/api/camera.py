from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.camera import Camera
from app.schemas.camera import CameraCreate, CameraResponse

router = APIRouter(prefix="/cameras", tags=["cameras"])

@router.post("/", response_model=CameraResponse)
def create_camera(camera: CameraCreate, db: Session = Depends(get_db)):
    db_camera = Camera(
        model=camera.model,
        location=camera.location,
    )
    db.add(db_camera)
    db.commit()
    db.refresh(db_camera)
    return db_camera

@router.get("/", response_model=list[CameraResponse])
def get_cameras(db: Session = Depends(get_db)):
    return db.query(Camera).all()