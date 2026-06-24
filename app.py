from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.health_route import router as health_router
from routes.websocket_route import router as websocket_router
from routes.ecg_route import router as ecg_router


app = FastAPI(
    title="ECG Stress Detection Backend",
    version="1.0.0"
)


# Allow frontend connection

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# Register routes

app.include_router(health_router)
app.include_router(websocket_router)
app.include_router(ecg_router)


@app.get("/")

def home():

    return {

        "message": "ECG Stress Detection Backend Running",
        "version": "1.0.0",
        "routes": [
            "/",
            "/health",
            "/ecg",
            "/ws"

        ]

    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True

    )