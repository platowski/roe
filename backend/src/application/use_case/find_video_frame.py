from adapters.out.openai import OpenaiAdapter
from application.use_case.capture_video_frames import CaptureVideoFramesUseCase

SYSTEM_PROMPT = "You are video processor that for a given frames from a video returns the frame that best matches the description. Return the frame number. Do not return any other information."


class FindVideoFrameUseCase:
    def __init__(self, openai_adapter: OpenaiAdapter):
        self.openai_adapter = openai_adapter

    async def execute(self, frame_description: str, filename: str):
        frames = await CaptureVideoFramesUseCase.execute(filename)
        frame_number = await self.openai_adapter.call_chat(
            SYSTEM_PROMPT,
            {"description": frame_description, "frames": frames},
            "gpt-4o",
        )
        # 'Let it fail' philosophy - if there is a problem then most likely we need investigate the prompt,
        # not parse data at all costs
        return frames[int(frame_number) - 1]
