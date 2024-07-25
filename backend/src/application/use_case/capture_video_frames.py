import cv2
import base64


class CaptureVideoFramesUseCase:
    @staticmethod
    async def execute(video_path: str):
        video = cv2.VideoCapture(video_path)

        fps = video.get(cv2.CAP_PROP_FPS)
        base64_frames = []
        while video.isOpened():
            success, frame = video.read()
            if not success:
                break
            _, buffer = cv2.imencode(".jpg", frame)
            base64_frames.append(base64.b64encode(buffer).decode("utf-8"))

        video.release()
        cv2.destroyAllWindows()
        # capturing all the frames would be too costly, so just 1 per second should be fine for most cases
        return base64_frames[::fps]
