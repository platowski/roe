from fastapi import UploadFile

from application.exceptions.video_processing import VideoProcessingException

UPLOADS_DIR = "uploads"


class StoreVideoUseCase:

    async def execute(self, uploaded_file: UploadFile) -> str:
        try:
            with open(self.get_video_path(uploaded_file.filename), "wb") as f:
                while contents := uploaded_file.file.read(1024 * 1024):
                    f.write(contents)
        except Exception:
            raise VideoProcessingException("There was an error uploading the file")
        finally:
            uploaded_file.file.close()
        return self.get_video_path(uploaded_file.filename)

    @staticmethod
    def get_video_path(filename) -> str:
        return f"{UPLOADS_DIR}/{filename}"
