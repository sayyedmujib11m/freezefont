from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from backend.freeze_font import freeze_font
from backend.inspect_font import inspect_font

from pathlib import Path
import shutil
import os
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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


@app.post("/inspect")
async def inspect_uploaded_font(
    file: UploadFile = File(...)
):

    upload_path = Path(UPLOAD_FOLDER) / file.filename

    with open(upload_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return inspect_font(str(upload_path))


@app.post("/upload")
async def upload_font(
    file: UploadFile = File(...),
    mode: str = Form("all"),
    selected_styles: str = Form("[]")
):

    upload_path = Path(UPLOAD_FOLDER) / file.filename

    with open(upload_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        selected_styles_list = json.loads(
            selected_styles
        )
    except:
        selected_styles_list = []

    zip_path = freeze_font(
        str(upload_path),
        OUTPUT_FOLDER,
        mode,
        selected_styles_list
    )

    return FileResponse(
        path=zip_path,
        filename=Path(zip_path).name,
        media_type="application/zip"
    )