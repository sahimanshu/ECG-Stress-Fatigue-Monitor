from fastapi import APIRouter, WebSocket

from websocket.websocket_handler import (
    handle_frontend,
    handle_esp32
)

router = APIRouter()


# Frontend WebSocket
@router.websocket("/ws/frontend")
async def frontend_socket(
    websocket: WebSocket
):

    await handle_frontend(
        websocket
    )


# ESP32 WebSocket
@router.websocket("/ws/esp32")
async def esp32_socket(
    websocket: WebSocket
):

    await handle_esp32(
        websocket
    )
