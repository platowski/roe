from fastapi import APIRouter, UploadFile

router = APIRouter(
    prefix="/video",
    tags=["video"],
    responses={
        404: {"description": "Not found"},
    },
)


@router.post("/upload", status_code=201)
async def post(file: UploadFile):
    try:
        with open("uploads/{}".format(file.filename), 'wb') as f:
            while contents := file.file.read(1024 * 1024):
                f.write(contents)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()
    return {"filename": file.filename}
