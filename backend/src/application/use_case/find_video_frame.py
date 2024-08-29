import torch
import logging

from PIL import Image
from transformers import CLIPModel,  AutoProcessor

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

        logits_per_text = outputs.logits_per_text  # this is the text-image similarity score
        probs_t = logits_per_text.softmax(dim=1).detach().numpy()

        most_similar_t_index = probs_t.argmax().item()
        return frames[most_similar_t_index]

        # frame_embeddings = await self.generate_video_embeddings(frames)
        # query_vector = await self.generate_query_vector(frame_description)

        # similarities = (query_vector @ frame_embeddings.T).squeeze(0)

        # Return the frame with the highest similarity
        # most_similar_frame_index = similarities.argmax().item()
        # return frames[most_similar_frame_index]

    # async def generate_query_vector(self, description):
    #     with torch.no_grad():
    #         # Preprocess the description to tokenize it
    #         text = self.tokenizer.tokenize(description)
    #         # Generate the embedding
    #         embedding = self.model.get_text_features(text)
    #     return embedding

    # async def generate_video_embeddings(self, frames):
    #     embeddings = []
    #     for frame in frames:
    #         with torch.no_grad():
    #             # For each frame in the chunk, preprocess and convert to tensor
    #             url = "http://images.cocodataset.org/val2017/000000039769.jpg"
    #             import requests
    #
    #             image = Image.open(requests.get(url, stream=True).raw)
    #             image_tensor = self.processor.preprocess(
    #                 images=image, return_tensors="pt"
    #             )
    #             # Generate the embedding
    #             embeddings.append(self.model(**image_tensor))
    #
    #         return torch.stack(embeddings)
