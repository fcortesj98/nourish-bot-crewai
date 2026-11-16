"""Image loading and encoding helpers shared by every vision tool."""

from __future__ import annotations

import base64
import mimetypes
import os
from typing import Optional

DEFAULT_MIME_TYPE = "image/jpeg"


def is_url(image_input: str) -> bool:
    return image_input.startswith(("http://", "https://"))


def load_image_bytes(image_input: str, timeout: Optional[int] = None) -> bytes:
    """Read an image from a local path or download it from a URL.

    :param image_input: Local file path or http(s) URL.
    :param timeout: Download timeout in seconds (defaults to settings).
    :raises FileNotFoundError: If a local path does not exist.
    """
    if is_url(image_input):
        import requests

        if timeout is None:
            from nourishbot.settings import get_settings

            timeout = get_settings().image_download_timeout
        response = requests.get(image_input, timeout=timeout)
        response.raise_for_status()
        return response.content

    if not os.path.isfile(image_input):
        raise FileNotFoundError(f"No file found at path: {image_input}")
    with open(image_input, "rb") as file:
        return file.read()


def guess_mime_type(image_input: str) -> str:
    mime, _ = mimetypes.guess_type(image_input.split("?")[0])
    return mime if mime and mime.startswith("image/") else DEFAULT_MIME_TYPE


def to_data_uri(image_bytes: bytes, mime_type: str = DEFAULT_MIME_TYPE) -> str:
    encoded = base64.b64encode(image_bytes).decode("utf-8")
    return f"data:{mime_type};base64,{encoded}"


def image_to_data_uri(image_input: str) -> str:
    """Load an image (path or URL) and return it as a base64 data URI."""
    return to_data_uri(load_image_bytes(image_input), guess_mime_type(image_input))


def save_pil_image_to_temp(image) -> str:
    """Save a PIL image to a unique temporary JPEG file and return its path.

    The original app always wrote ``uploaded_image.jpg`` in the working
    directory, so simultaneous users overwrote each other's uploads and PNGs
    with transparency failed to save. A unique temp file fixes both.
    """
    import tempfile

    if image.mode not in ("RGB", "L"):
        image = image.convert("RGB")
    fd, path = tempfile.mkstemp(prefix="nourishbot_", suffix=".jpg")
    os.close(fd)
    image.save(path, format="JPEG")
    return path
