import cv2


class CaptureVideoFramesUseCase:
    @staticmethod
    async def execute(video_path: str):
        video = cv2.VideoCapture(video_path)

        fps = video.get(cv2.CAP_PROP_FPS)
        frames = []
        while video.isOpened():
            success, frame = video.read()
            if not success:
                break
            frames.append(frame)

        video.release()
        cv2.destroyAllWindows()
        # capturing all the frames would be too costly, so just 1 per second should be fine for most cases
        return frames[0:: int(fps)]
