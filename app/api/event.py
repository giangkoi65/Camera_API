import shutil
import os
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.event import Event
from app.models.camera import Camera
from app.schemas.event import EventCreate, EventResponse, EventWithCameraResponse

from app.db.mongo import event_logs_collection
from app.schemas.event_log import EventLogCreate
from datetime import datetime, timezone
from bson import ObjectId

from app.services.image_service import process_image


router = APIRouter(prefix="/events", tags=["events"])

events = []
event_id_counter = 1

@router.post("/", response_model=EventResponse)
def create_event(event: EventCreate, db: Session = Depends(get_db)):
    camera = db.query(Camera).filter(Camera.id == event.camera_id).first()
    if not camera:
        raise HTTPException(status_code=404, detail="Camera not found")
    
    db_event = Event(
        camera_id=event.camera_id,
        event_type=event.event_type,
        description=event.description
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

@router.get("/", response_model=list[EventResponse])
def get_events(db: Session = Depends(get_db)):
    return db.query(Event).all()

@router.get("/camera/{camera_id}", response_model=list[EventWithCameraResponse])
def get_events_by_camera(camera_id: int, db: Session = Depends(get_db)):
    result = (
        db.query(Event, Camera)
        .join(Camera, Event.camera_id == Camera.id)
        .filter(Camera.id == camera_id)
        .all()
    )

    return [
        {
            "event_id": e.id,
            "event_type": e.event_type,
            "camera_model": c.model,
            "location": c.location,
            "created_at": e.created_at
        }
        for e, c in result
    ]
    
@router.post("{event_id}/log/")
def log_event_to_mongo(event_id: int, log: EventLogCreate):
    document = {
        "event_id": event_id,
        "objects": log.objects,
        "confidence": log.confidence,
        "image_path": log.image_path,
        "extra": log.extra,
        "created_at": datetime.now(timezone.utc)
    }
    
    result = event_logs_collection.insert_one(document)
    
    return {
        "message": "Event log stored successfully",
        "log_id": str(result.inserted_id)
    }
    
@router.get("{event_id}/log/")
def get_event_logs_from_mongo(event_id: int):
    logs = event_logs_collection.find({"event_id": event_id})
    
    return [
        {
            "log_id": str(log["_id"]),
            "event_id": log["event_id"],
            "objects": log["objects"],
            "confidence": log["confidence"],
            "image_path": log["image_path"],
            "extra": log["extra"],
            "created_at": log["created_at"]
        }
        for log in logs
    ]
    
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/{event_id}/upload-image")
def upload_event_image(
    event_id: int,
    file: UploadFile = File(...)
):
    file_path = f"{UPLOAD_DIR}/event_{event_id}_{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    image_metadata = process_image(file_path)

    log_document = {
        "event_id": event_id,
        "image_path": file_path,
        "image_metadata": image_metadata,
        "created_at": datetime.utcnow()
    }

    event_logs_collection.insert_one(log_document)

    return {
        "message": "Image uploaded and processed",
        "image_metadata": image_metadata
    }