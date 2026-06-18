from fastapi import FastAPI, UploadFile, File
from backend.freeze_font import freeze_font
from pathlib import Path
import shutil
import os

app = FastAPI()

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "output"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.get("/")
def home():
    return {
        "app": "FreezeFont",
        "status": "running"
    }

@app.post("/upload")
async def upload_font(file: UploadFile = File(...)):
    upload_path = Path(UPLOAD_FOLDER) / file.filename

    with open(upload_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    zip_path = freeze_font(
        str(upload_path),
        OUTPUT_FOLDER
    )

    return {
        "success": True,
        "filename": file.filename,
        "zip_file": zip_path
    }