import os
import uuid
from pathlib import Path

UPLOAD_FOLDER = Path("uploads")
UPLOAD_FOLDER.mkdir(exist_ok=True)

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
MAX_FILE_SIZE = 5 * 1024 * 1024

def save_file(file_content: bytes, original_filename: str) -> dict:
    ext = os.path.splitext(original_filename)[1].lower()
    
    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError(f"Неподдерживаемый формат. Разрешены: {', '.join(ALLOWED_EXTENSIONS)}")
    
    if len(file_content) > MAX_FILE_SIZE:
        raise ValueError(f"Файл слишком большой. Максимум {MAX_FILE_SIZE // 1024 // 1024} MB")
    
    unique_name = f"{uuid.uuid4().hex}{ext}"
    file_path = UPLOAD_FOLDER / unique_name
    
    with open(file_path, "wb") as f:
        f.write(file_content)
    
    return {
        "url": f"/uploads/{unique_name}",
        "file_name": original_filename,
        "file_size": len(file_content),
        "content_type": f"image/{ext[1:]}"
    }

def delete_file(file_url: str) -> bool:
    if file_url.startswith("/uploads/"):
        file_name = file_url.replace("/uploads/", "")
        file_path = UPLOAD_FOLDER / file_name
        if file_path.exists():
            os.remove(file_path)
            return True
    return False