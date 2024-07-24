import logging
from fastapi import FastAPI

from ports.into.status_response import StatusResponse
from adapters.into.http.video import router as video_router


logger = logging.getLogger("uvicorn.error")


app = FastAPI(title="API for Sample App")
app.include_router(video_router)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/health_check", response_model=StatusResponse)
async def health_check():
    return StatusResponse(message="OK")


base_host = "0.0.0.0"
base_port = 8008

if __name__ == "__main__":
    app.run(host=base_host, port=base_port)
