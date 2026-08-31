import os
from typing import Tuple
from fastapi import UploadFile
from app.config import settings
from app.utils.files import sanitize_filename, validate_image_file


class StorageService:
    def __init__(self, upload_dir: str = settings.UPLOAD_DIR, report_dir: str = settings.REPORT_DIR):
        self.upload_dir = upload_dir
        self.report_dir = report_dir
        os.makedirs(self.upload_dir, exist_ok=True)
        os.makedirs(self.report_dir, exist_ok=True)

    async def save_image(self, file: UploadFile) -> Tuple[str, str, int, int, bytes]:
        """
        Validates and saves an uploaded image file.
        Returns: (file_name, storage_path, width, height, raw_bytes)
        """
        contents = await file.read()
        width, height = validate_image_file(file, contents)
        
        safe_filename = sanitize_filename(file.filename or "upload.jpg")
        file_path = os.path.join(self.upload_dir, safe_filename)
        
        with open(file_path, "wb") as f:
            f.write(contents)
            
        return safe_filename, file_path, width, height, contents

    def get_image_path(self, file_name: str) -> str:
        return os.path.join(self.upload_dir, file_name)

    def get_report_path(self, file_name: str) -> str:
        return os.path.join(self.report_dir, file_name)


storage_service = StorageService()
