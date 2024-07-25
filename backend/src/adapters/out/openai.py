import openai
import json
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
    retry_if_not_exception_type,
)
from utils.env import env_settings


class OpenaiAdapter:
    def __init__(self):
        self.client = openai.AsyncClient(api_key=env_settings.gpt_key)

    @staticmethod
    def check_status() -> bool:
        return len(openai.Model.list()) > 0

    async def call_chat(
        self, prompt: str, data, model_name: str, temperature=None
    ) -> str:
        if not isinstance(data, str):
            data = json.dumps(data)
        # Construct the 'messages' parameter as a list of dictionaries.
        # The list includes both system and user messages.
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": data},
        ]

        # Initialize a dictionary with the model type and messages to send in the API call.
        api_params = {"model": model_name, "messages": messages, "max_tokens": 500}

        # If the 'temperature' parameter is provided, add it to 'api_params'.
        if temperature is not None:
            api_params["temperature"] = temperature

        try:
            response = await self.call_with_backoff(
                self.client.chat.completions.create, **api_params
            )

            # Extract the generated content from the API response.
            # The 'strip()' function removes any leading/trailing white spaces.
            response_content = response["choices"][0]["message"].content.strip()

            return response_content

        except Exception as e:
            raise RuntimeError(f"An error occurred while making an API call: {e}")

    @classmethod
    async def completions_with_backoff(cls, **kwargs):
        return await cls.call_with_backoff(openai.Completion.acreate, **kwargs)

    @staticmethod
    @retry(
        wait=wait_random_exponential(min=1, max=60),
        stop=stop_after_attempt(3),
        retry=retry_if_not_exception_type(openai.BadRequestError),
    )
    async def call_with_backoff(fn, **kwargs):
        return await fn(**kwargs)
