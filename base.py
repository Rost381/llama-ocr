import os
import base64
import requests
from typing import Literal, Optional, TypedDict, Union

ModelType = Literal["Llama-Vision-Free", "Llama-3.2-11B-Vision", "Llama-3.2-90B-Vision"]


class OCRResult(TypedDict):
    markdown: str
    raw_response: dict
    model_used: str
    is_free_model: bool


def is_remote_file(file_path: str) -> bool:
    return file_path.startswith(("http://", "https://"))

def encode_image(image_path: str) -> str:
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def get_system_prompt() -> str:
    """System prompt for OCR"""
    return """Convert the image to Markdown. Include all content:
- Headers, footers, subtexts
- Images with alt text
- Tables and other elements
Output ONLY Markdown without any additional text or delimiters."""


def ocr(
        file_path: str,
        api_key: Optional[str] = os.getenv("TOGETHER_API_KEY"),
        model: ModelType = "Llama-Vision-Free",
        return_markdown: bool = False
) -> Union[str, OCRResult]:
    """
    Convert image to Markdown/JSON

    Args:
        file_path: Image path or URL
        api_key: API key Together AI
        model: model
        return_markdown: If True - only Markdown

    Returns:
        Markdown or JSON
    """
    model_mapping = {
        "Llama-Vision-Free": "meta-llama/Llama-Vision-Free",
        "Llama-3.2-11B-Vision": "meta-llama/Llama-3.2-11B-Vision-Instruct-Turbo",
        "Llama-3.2-90B-Vision": "meta-llama/Llama-3.2-90B-Vision-Instruct-Turbo"
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    image_url = (
        file_path if is_remote_file(file_path)
        else f"data:image/png;base64,{encode_image(file_path)}"
    )

    payload = {
        "model": model_mapping[model],
        "messages": [{
            "role": "user",
            "content": [
                {"type": "text", "text": get_system_prompt()},
                {"type": "image_url", "image_url": {"url": image_url}}
            ]
        }]
    }

    response = requests.post(
        "https://api.together.xyz/v1/chat/completions",
        headers=headers,
        json=payload
    )
    response.raise_for_status()

    response_data = response.json()
    markdown = response_data["choices"][0]["message"]["content"]

    if return_markdown:
        return markdown

    return {
        "markdown": markdown,
        "raw_response": response_data,
        "model_used": model,
        "is_free_model": model == "Llama-Vision-Free"
    }