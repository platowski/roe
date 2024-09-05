from typing import List

import cv2
import numpy as np

FrameCollection = List[np.ndarray]


class CaptureVideoFramesUseCase:
    @staticmethod
    async def execute(video_path: str) -> FrameCollection:
        video = cv2.VideoCapture(video_path)

        fps = video.get(cv2.CAP_PROP_FPS)
        frames = []
        while video.isOpened():
            success, frame = video.read()
            if not success:
                break
            # @todo resize the frame to a smaller size to reduce the processing
            frames.append(frame)

        video.release()
        cv2.destroyAllWindows()
        # capturing all the frames would be too costly, so just 1 per second should be fine for most cases
        return frames[0 :: int(fps)]
