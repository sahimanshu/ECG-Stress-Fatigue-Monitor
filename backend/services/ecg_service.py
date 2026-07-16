from websocket.websocket_handler import ecg_buffer, broadcast
from services.feature_extractor import extract_features
from services.ml_client import predict_stress
from services.stress_service import get_stress_level

SAMPLING_RATE = 700
WINDOW_SEC = 180

# Ideal 3-minute window
WINDOW_SIZE = SAMPLING_RATE * WINDOW_SEC

# Allow 2% packet loss
MIN_WINDOW_SIZE = int(WINDOW_SIZE * 0.98)

# Keep last 1.5 minutes after prediction
STEP_SIZE = WINDOW_SIZE // 2

print("=" * 60)
print("Target Window Size :", WINDOW_SIZE)
print("Minimum Window Size:", MIN_WINDOW_SIZE)
print("Sliding Window Size:", STEP_SIZE)
print("=" * 60)


async def process_ecg(ecg_values, electrode_connected):

    print("=" * 60)
    print("New ECG Batch Received")
    print("Batch Size:", len(ecg_values))
    print("Electrode Connected:", electrode_connected)

    # Electrode disconnected
    if not electrode_connected:

        print("Electrode disconnected")
        print("Buffer Cleared")

        ecg_buffer.clear()

        return {
            "status": "electrodes_not_connected"
        }

    # Process every ECG sample
    for ecg in ecg_values:

        # Send live ECG to frontend
        await broadcast(
            {
                "type": "ecg",
                "ecg": ecg,
                "electrode_connected": electrode_connected
            }
        )

        ecg_buffer.append(ecg)

    print("Current Buffer Size:", len(ecg_buffer))

    # Wait until enough ECG collected
    if len(ecg_buffer) < MIN_WINDOW_SIZE:

        print(
            f"Recording... {len(ecg_buffer)}/{MIN_WINDOW_SIZE}"
        )

        return {
            "status": "recording",
            "samples": len(ecg_buffer)
        }

    print("=" * 60)
    print("Minimum required samples reached")
    print("Available Samples:", len(ecg_buffer))

    try:

        print("=" * 60)
        print("Starting Feature Extraction")

        # Use available samples (up to the ideal window size)
        window = ecg_buffer[-min(len(ecg_buffer), WINDOW_SIZE):]

        print("Window Used For Extraction:", len(window))

        features = extract_features(
            window,
            SAMPLING_RATE
        )

        print("Feature Extraction Completed")
        print(features)

        print("=" * 60)
        print("Calling ML API")

        result = predict_stress(features)

        print("ML Response")
        print(result)

        stress_score = result["stress_probability"]

        stress_level = get_stress_level(
            stress_score
        )

        print("Stress Score:", stress_score)
        print("Stress Level:", stress_level)

        await broadcast(
            {
                "type": "prediction",
                "stress_score": stress_score,
                "stress_level": stress_level,
                "hr": features["HR"]
            }
        )

        print("Prediction Sent To Frontend")

        # Sliding window
        del ecg_buffer[:-STEP_SIZE]

        print("Buffer Updated")
        print("Current Buffer Size:", len(ecg_buffer))

        return {
            "status": "prediction_sent"
        }

    except Exception as e:

        print("=" * 60)
        print("Prediction Error")
        print(e)

        return {
            "status": "error",
            "message": str(e)
        }
