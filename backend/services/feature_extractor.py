import numpy as np
import neurokit2 as nk


def extract_features(
    ecg_signal,
    sampling_rate=700
):

    print("=" * 60)
    print("Feature Extraction Started")

    ecg_signal = np.array(ecg_signal)

    print("Window Size:", len(ecg_signal))
    print("First 10 Raw ECG Samples:", ecg_signal[:10])

    # ==============================
    # ECG Processing
    # ==============================

    signals, info = nk.ecg_process(
        ecg_signal,
        sampling_rate=sampling_rate
    )

    print("ECG Cleaning Completed")
    print(
        "First 10 Clean ECG Samples:",
        signals["ECG_Clean"][:10].tolist()
    )

    print(
        "R Peaks Detected:",
        len(info["ECG_R_Peaks"])
    )

    # ==============================
    # HRV Time Domain
    # ==============================

    hrv_time = nk.hrv_time(
        info["ECG_R_Peaks"],
        sampling_rate=sampling_rate,
        show=False
    )

    print("Time Domain Features Calculated")

    # ==============================
    # HRV Frequency Domain
    # ==============================

    hrv_freq = nk.hrv_frequency(
        info["ECG_R_Peaks"],
        sampling_rate=sampling_rate,
        show=False
    )

    print("Frequency Domain Features Calculated")

    # ==============================
    # HRV Nonlinear
    # ==============================

    hrv_nonlinear = nk.hrv_nonlinear(
        info["ECG_R_Peaks"],
        sampling_rate=sampling_rate,
        show=False
    )

    print("Nonlinear Features Calculated")

    # ==============================
    # Feature Dictionary
    # ==============================

    features = {

        "HR": float(
            signals["ECG_Rate"].mean()
        ),

        "MeanNN": float(
            hrv_time["HRV_MeanNN"].iloc[0]
        ),

        "SDNN": float(
            hrv_time["HRV_SDNN"].iloc[0]
        ),

        "RMSSD": float(
            hrv_time["HRV_RMSSD"].iloc[0]
        ),

        "pNN50": float(
            hrv_time["HRV_pNN50"].iloc[0]
        ),

        "LF": float(
            hrv_freq["HRV_LF"].iloc[0]
        ),

        "HF": float(
            hrv_freq["HRV_HF"].iloc[0]
        ),

        "LFHF": float(
            hrv_freq["HRV_LFHF"].iloc[0]
        ),

        "SD1": float(
            hrv_nonlinear["HRV_SD1"].iloc[0]
        ),

        "SD2": float(
            hrv_nonlinear["HRV_SD2"].iloc[0]
        ),

        "ECG_Quality": float(
            signals["ECG_Quality"].mean()
        )

    }

    print("=" * 60)
    print("Extracted Features")

    for key, value in features.items():
        print(f"{key}: {value}")

    # ==============================
    # Validation
    # ==============================

    for key, value in features.items():

        if not np.isfinite(value):

            raise Exception(
                f"{key} is invalid"
            )

    if features["HR"] < 40:
        raise Exception("HR too low")

    if features["HR"] > 200:
        raise Exception("HR too high")

    if features["RMSSD"] <= 0:
        raise Exception("Invalid RMSSD")

    if features["SDNN"] <= 0:
        raise Exception("Invalid SDNN")

    if features["LF"] < 0:
        raise Exception("Invalid LF")

    if features["HF"] < 0:
        raise Exception("Invalid HF")

    if features["LFHF"] < 0:
        raise Exception("Invalid LFHF")

    print("=" * 60)
    print("Feature Extraction Successful")
    print("=" * 60)

    return features
