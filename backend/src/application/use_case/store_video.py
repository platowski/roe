from fastapi import UploadFile

UPLOADS_DIR = "uploads"


class StoreVideoUseCase:

    async def execute(self, file: UploadFile):
        try:
            with open(self.get_video_path(file.filename), "wb") as f:
                while contents := file.file.read(1024 * 1024):
                    f.write(contents)
        except Exception:
            return {"message": "There was an error uploading the file"}
        finally:
            file.file.close()
        return self.get_video_path(file.filename)

    @staticmethod
    def get_video_path(filename):
        return f"{UPLOADS_DIR}/{filename}"
