from fastapi import APIRouter, WebSocket
from websocket.websocket_handler import handle_websocket

router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket
):

    await handle_websocket(
        websocket
    )