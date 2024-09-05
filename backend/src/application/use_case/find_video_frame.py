from concurrent.futures.process import ProcessPoolExecutor
from typing import List

import torch
import logging
import numpy as np

from transformers import CLIPModel, AutoProcessor
from utils.env import env_settings
from application.use_case.capture_video_frames import (
    CaptureVideoFramesUseCase,
    FrameCollection,
)

CLIP_MODEL_NAME = "openai/clip-vit-base-patch32"

logger = logging.getLogger("uvicorn.error")


class FindVideoFrameUseCase:
    def __init__(self):
        self.model = CLIPModel.from_pretrained(CLIP_MODEL_NAME)
        self.processor = AutoProcessor.from_pretrained(CLIP_MODEL_NAME)

        self.device = "cuda" if torch.cuda.is_available() else "cpu"

    async def execute(self, frame_description: str, filename: str) -> np.ndarray:
        frames = await CaptureVideoFramesUseCase.execute(filename)
        text_embeddings = self.get_text_embeddings(frame_description)
        frame_embeddings = self.get_frame_embeddings(frames)

        text_embeddings = torch.tensor(text_embeddings).to(self.device)
        frame_embeddings = torch.tensor(frame_embeddings).to(self.device)
        # @todo store video embeddings (vector DB, pinecone) and the video to allow multiple searches among single file

        similarities = torch.matmul(frame_embeddings, text_embeddings.T).squeeze()
        best_frame_index = torch.argmax(similarities).item()

        return frames[best_frame_index]

    def get_text_embeddings(self, text: str) -> np.ndarray:
        inputs = self.processor(text=[text], return_tensors="pt", padding=True)
        inputs = {k: v.to(self.device) for k, v in inputs.items()}

        with torch.no_grad():
            text_features = self.model.get_text_features(**inputs)

        return text_features.cpu().numpy()

    def get_embeddings_for_frames_chunk(self, chunk: FrameCollection) -> np.ndarray:
        inputs = self.processor(images=chunk, return_tensors="pt", padding=True)
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        with torch.no_grad():
            frame_features = self.model.get_image_features(**inputs)
        return frame_features.cpu().numpy()

    @staticmethod
    def split_frames_into_chunks(
        frames: FrameCollection, number_of_chunks: int
    ) -> List[FrameCollection]:
        chunk_size = -(len(frames) // -number_of_chunks)  # round up division
        return [frames[i : i + chunk_size] for i in range(0, len(frames), chunk_size)]

    def get_frame_embeddings(self, frames: FrameCollection) -> torch.Tensor:
        chunks = self.split_frames_into_chunks(frames, env_settings.cpu_count)
        logger.info(
            f"Processing {len(chunks)} chunks with, cpu count {env_settings.cpu_count}"
        )

        results = []
        with ProcessPoolExecutor(max_workers=env_settings.cpu_count) as executor:
            for result in executor.map(self.get_embeddings_for_frames_chunk, chunks):
                results.append(result)
                logger.info(f"Processed chunk with shape {result.shape}")

        # Combine results from all chunks
        frame_features = torch.cat(results, dim=0)
        return frame_features

    async def execute_legacy(self, frame_description: str, filename: str):
        frames = await CaptureVideoFramesUseCase.execute(filename)

        logger.error(f"Processing {len(frames)} frames")

        inputs = self.processor(
            text=[frame_description], images=frames, return_tensors="pt", padding=True
        )

        outputs = self.model(**inputs)

        logits_per_text = outputs.logits_per_text
        probs_t = logits_per_text.softmax(dim=1).detach().numpy()

        most_similar_t_index = probs_t.argmax().item()

        return frames[most_similar_t_index]
