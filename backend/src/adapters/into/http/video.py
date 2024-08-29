from fastapi import APIRouter, UploadFile
import logging

from starlette.responses import FileResponse

from application.use_case.find_video_frame import FindVideoFrameUseCase
from application.use_case.prepare_frame_for_download import PrepareFrameForDownloadUseCase
from application.use_case.store_video import StoreVideoUseCase

router = APIRouter(
    prefix="/video",
    tags=["video"],
    responses={
        404: {"description": "Not found"},
    },
)

logger = logging.getLogger(__name__)


@router.post("/upload", status_code=201)
async def post(
    file: UploadFile,
    user_question: str,
):
    logger.error(f"start processing video")
    store_video_use_case = StoreVideoUseCase()
    filename = await store_video_use_case.execute(file)
    find_video_frame_use_case = FindVideoFrameUseCase()
    frame = await find_video_frame_use_case.execute(user_question, filename)
    file_location = PrepareFrameForDownloadUseCase.execute(frame)
    return FileResponse(file_location, media_type='application/octet-stream', filename='frame.jpg')
