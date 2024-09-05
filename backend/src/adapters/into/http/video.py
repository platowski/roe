from fastapi import APIRouter, UploadFile

from starlette.responses import FileResponse

from application.use_case.find_video_frame import FindVideoFrameUseCase
from application.use_case.prepare_frame_for_download import (
    PrepareFrameForDownloadUseCase,
)
from application.use_case.store_video import StoreVideoUseCase

router = APIRouter(
    prefix="/video",
    tags=["video"],
    responses={
        404: {"description": "Not found"},
    },
)


# @todo split this into video upload/list videos/search
@router.post("/search", status_code=201)
async def post(
    file: UploadFile,
    user_question: str,
):
    """
    Upload a video file and search for a frame that matches the user's question
    This endpoint will be deprecated in the future, as the video upload and frame search will be split into separate endpoints
    For now, it's a good way to test the whole process as there is no frontend application to provide proper user experience
    """
    store_video_use_case = StoreVideoUseCase()
    filename = await store_video_use_case.execute(file)
    # @todo move FindVideoFrameUseCase.get_frame_embeddings to a background task that runs after the video is uploaded
    find_video_frame_use_case = FindVideoFrameUseCase()
    frame = await find_video_frame_use_case.execute(user_question, filename)
    file_location = PrepareFrameForDownloadUseCase.execute(frame)
    return FileResponse(
        file_location, media_type="application/octet-stream", filename="frame.jpg"
    )
