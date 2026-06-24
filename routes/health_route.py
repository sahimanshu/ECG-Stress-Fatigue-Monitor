from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health():

    return {

        "status": "OK",

        "service": "ECG Stress Detection Backend"

    }