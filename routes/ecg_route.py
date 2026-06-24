from fastapi import APIRouter
from pydantic import BaseModel
from websocket.websocket_handler import (ecg_buffer,broadcast)
from services.feature_extractor import extract_features
from services.ml_client import predict_stress
from services.stress_service import get_stress_level


router = APIRouter()




SAMPLING_RATE = 700
WINDOW_SEC = 180          # 3 min
WINDOW_SIZE = SAMPLING_RATE * WINDOW_SEC
STEP_SIZE = WINDOW_SIZE // 2     



class ECGData(BaseModel):
    ecg: float
    electrode_connected: bool
    
@router.post("/ecg")

async def receive_ecg(data: ECGData):

    global ecg_buffer


    # Send live ECG + connection status to frontend

    await broadcast(

        {
            "type":"ecg",
            "ecg":data.ecg,
            "electrode_connected":data.electrode_connected
        }

    )


    # Electrodes detached

    if not data.electrode_connected:
        ecg_buffer.clear()


        return {"status":"electrodes_not_connected"}


    # Store ECG sample

    ecg_buffer.append(data.ecg)


    # Wait until enough ECG collected

    if len(ecg_buffer) < WINDOW_SIZE:


        return {
            "status":
            "recording",
            "samples":
            len(ecg_buffer)

        }


    try:
        print("Extracting Features...")

        # Take latest 3 min ECG

        window = ecg_buffer[-WINDOW_SIZE:]


        # Feature Extraction

        features = extract_features(window,SAMPLING_RATE)
        print("Calling ML API...")


        # ML Prediction

        result = predict_stress(features)


        stress_score = result["stress_probability"]


        # Convert to

        # Low / Moderate / High

        stress_level = get_stress_level(stress_score)


        print("Prediction:",stress_score,stress_level)


        # Send prediction to frontend

        await broadcast(

            {
                "type":"prediction",
                "stress_score":stress_score,
                "stress_level":stress_level,
                "hr":features["HR"]

            }

        )


        # Keep last 1.5 min ECG

        del ecg_buffer[:-STEP_SIZE]


        return { "status": "prediction_sent"}


    except Exception as e:


        print("Prediction Error:",e)


        return {
            "status":
            "error",
            "message":
            str(e)
        }