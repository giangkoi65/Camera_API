from fastapi import FastAPI
from app.api import camera, event
from app.schemas.camera import CameraCreate, CameraResponse
from app.api.websocket import router as websocket_router

app = FastAPI(title="Smart Camera API")
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