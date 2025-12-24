from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api import camera, event
from app.schemas.camera import CameraCreate, CameraResponse
from app.api.websocket import router as websocket_router
from app.db.init_db import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Khởi tạo database khi ứng dụng bắt đầu
    print("Starting up: Initializing database...")
    init_db()
    yield
    # Bạn có thể thêm code dọn dẹp (nếu cần) ở đây sau lệnh yield
    print("Shutting down...")

app = FastAPI(title="Smart Camera API", lifespan=lifespan)
# items = [
#     CameraCreate(model="CamModelX", location="Entrance"),
#     CameraCreate(model="CamModelY", location="Lobby"),
#     CameraResponse(id=1, model="CamModelX", location="Entrance", resolution="1920x1080", status="active"),
# ]
items = []



@app.get("/")
def root():
    return {"Hello": "World"}

# @app.get("/items")
# def get_items():
#     return {"items": items}


# @app.post("/items")
# def create_item(name: str):
#     items.append(name)
#     return {"item": name}

app.include_router(camera.router)
app.include_router(event.router)
app.include_router(websocket_router)