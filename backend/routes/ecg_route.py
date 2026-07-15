from fastapi import APIRouter
from pydantic import BaseModel

from services.ecg_service import process_ecg

router = APIRouter()


class ECGData(BaseModel):
    ecg: float
    electrode_connected: bool


@router.post("/ecg")
async def receive_ecg(data: ECGData):

    return await process_ecg(
        data.ecg,
        data.electrode_connected
    )
