import torch
import logging

from transformers import CLIPModel, AutoProcessor

from application.use_case.capture_video_frames import CaptureVideoFramesUseCase

CLIP_MODEL_NAME = "openai/clip-vit-base-patch32"

logger = logging.getLogger(__name__)


class FindVideoFrameUseCase:
    def __init__(self):
        self.model = CLIPModel.from_pretrained(CLIP_MODEL_NAME)
        self.processor = AutoProcessor.from_pretrained(CLIP_MODEL_NAME)

        self.device = "cuda" if torch.cuda.is_available() else "cpu"

    async def execute(self, frame_description: str, filename: str):
        frames = await CaptureVideoFramesUseCase.execute(filename)

        logger.error(f"Processing {len(frames)} frames")

        inputs = self.processor(
            text=[frame_description], images=frames, return_tensors="pt", padding=True
        )
        logger.error(f"Inputs generated")
        outputs = self.model(**inputs)

        logits_per_text = outputs.logits_per_text
        probs_t = logits_per_text.softmax(dim=1).detach().numpy()

        most_similar_t_index = probs_t.argmax().item()
        return frames[most_similar_t_index]
