import os
import re
import uuid
from typing import Tuple
from fastapi import UploadFile, HTTPException, status
from PIL import Image
import io
from app.config import settings

ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
ALLOWED_MIME_TYPES = {"image/jpeg", "image/png", "image/webp"}
MAX_FILE_BYTES = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024


def sanitize_filename(filename: str) -> str:
    """Sanitize and generate a collision-safe filename while keeping original extension."""
    name, ext = os.path.splitext(filename)
    ext = ext.lower()
    clean_name = re.sub(r"[^a-zA-Z0-9_\-]", "_", name)[:40]
    unique_suffix = uuid.uuid4().hex[:8]
    return f"{clean_name}_{unique_suffix}{ext}"


def validate_image_file(file: UploadFile, contents: bytes) -> Tuple[int, int]:
    """
    Validate image file size, extension, MIME type, and real image headers.
    Returns (width, height) of the image.
    """
    # 1. Size check
    if len(contents) > MAX_FILE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail={
                "code": "IMAGE_TOO_LARGE",
                "message": f"Maximum image size is {settings.MAX_UPLOAD_SIZE_MB} MB.",
            },
        )

    # 2. Extension check
    _, ext = os.path.splitext(file.filename or "")
    if ext.lower() not in ALLOWED_IMAGE_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": "INVALID_FILE_TYPE",
                "message": f"Unsupported file extension '{ext}'. Allowed: {', '.join(ALLOWED_IMAGE_EXTENSIONS)}",
            },
        )

    # 3. Content-Type check
    if file.content_type and file.content_type.lower() not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": "INVALID_MIME_TYPE",
                "message": f"Unsupported MIME type '{file.content_type}'. Allowed: {', '.join(ALLOWED_MIME_TYPES)}",
            },
        )

    # 4. Actual image payload validation using Pillow
    try:
        with Image.open(io.BytesIO(contents)) as img:
            img.verify()
            width, height = img.size
            if width <= 0 or height <= 0:
                raise ValueError("Invalid dimensions")
            return width, height
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": "CORRUPTED_IMAGE",
                "message": f"Uploaded file is corrupted or not a valid image: {str(e)}",
            },
        )
