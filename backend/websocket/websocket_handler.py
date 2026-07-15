from fastapi import WebSocket
from typing import List

from services.ecg_service import process_ecg

# Connected frontend clients
latest_clients: List[WebSocket] = []

# Shared ECG buffer
ecg_buffer = []


# ==========================================
# Frontend WebSocket
# ==========================================
async def handle_frontend(websocket: WebSocket):

    await websocket.accept()
    latest_clients.append(websocket)

    print("Frontend Connected")

    try:

        while True:

            # Keep frontend connection alive
            await websocket.receive_text()

    except Exception:

        print("Frontend Disconnected")

        if websocket in latest_clients:
            latest_clients.remove(websocket)


# ==========================================
# ESP32 WebSocket
# ==========================================
async def handle_esp32(websocket: WebSocket):

    await websocket.accept()

    print("ESP32 Connected")

    try:

        while True:

            # Receive JSON from ESP32
            data = await websocket.receive_json()

            # Validate packet
            if (
                "ecg" not in data or
                "electrode_connected" not in data
            ):

                print("Invalid Packet Received")
                continue

            print("=" * 60)
            print("ECG Batch Received From ESP32")
            print("Batch Size:", len(data["ecg"]))
            print("Electrode Connected:", data["electrode_connected"])
            print("First 5 Samples:", data["ecg"][:5])

            # Process ECG Batch
            result = await process_ecg(
                data["ecg"],
                data["electrode_connected"]
            )

            print("Processing Status:", result["status"])

    except Exception as e:

        print("ESP32 Disconnected")
        print("Reason:", e)


# ==========================================
# Broadcast To Frontend
# ==========================================
async def broadcast(data: dict):

    disconnected = []

    for ws in latest_clients:

        try:

            await ws.send_json(data)

        except Exception:

            disconnected.append(ws)

    for ws in disconnected:

        if ws in latest_clients:
            latest_clients.remove(ws)
