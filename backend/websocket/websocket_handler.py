from fastapi import WebSocket
from typing import List


# Connected frontend clients
latest_clients: List[WebSocket] = []


# Shared ECG buffer
ecg_buffer = []


async def handle_websocket(websocket: WebSocket):

    await websocket.accept()
    latest_clients.append(websocket)

    print("Frontend Connected")

    try:

        while True:
            # Keep connection alive
            await websocket.receive_text()


    except Exception:

        print("Frontend Disconnected")

        if websocket in latest_clients:
            latest_clients.remove(websocket)


async def broadcast(data: dict):

    disconnected = []
    for ws in latest_clients:
        try:
            await ws.send_json(data)

        except Exception:
            disconnected.append(ws)


    for ws in disconnected:
        latest_clients.remove(ws)