from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.ws_manager import ConnectionManager

router = APIRouter()
manager = ConnectionManager()

@router.websocket("/ws/events")
async def websocket_events(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Echo: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)