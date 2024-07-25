from typing import Annotated

from fastapi import APIRouter, UploadFile, Depends

from adapters.out import openai
from application.use_case.find_video_frame import FindVideoFrameUseCase
from application.use_case.store_video import StoreVideoUseCase

router = APIRouter(
    prefix="/video",
    tags=["video"],
    responses={
        404: {"description": "Not found"},
    },
)


@router.post("/upload", status_code=201)
async def post(
    file: UploadFile,
    user_question: str,
    openai_adapter: Annotated[openai.OpenaiAdapter, Depends(openai.OpenaiAdapter)],
):
    store_video_use_case = StoreVideoUseCase()
    filename = await store_video_use_case.execute(file)
    find_video_frame_use_case = FindVideoFrameUseCase(openai_adapter)
    return await find_video_frame_use_case.execute(user_question, filename)
