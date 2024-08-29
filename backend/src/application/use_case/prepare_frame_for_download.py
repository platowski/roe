import cv2


class PrepareFrameForDownloadUseCase:
    @staticmethod
    def execute(frame):
        file_location = "uploads/frame.jpg"
        cv2.imwrite(file_location, frame)
        return file_location
