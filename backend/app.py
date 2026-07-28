from pathlib import Path
import json
import shutil
from uuid import uuid4

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from backend.services.freeze_font import freeze_font
from backend.services.inspect_font import inspect_font

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "fontend"
UPLOAD_FOLDER = BASE_DIR / "uploads" / "runtime"
OUTPUT_FOLDER = BASE_DIR / "output" / "runtime"

UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

app = FastAPI(
    title="FreezeFont",
    description="Inspect variable fonts and convert their named instances into static TTF files.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def save_upload(file: UploadFile) -> Path:
    original_name = Path(file.filename or "font.ttf").name
    upload_name = f"{uuid4().hex}-{original_name}"
    upload_path = UPLOAD_FOLDER / upload_name

    with upload_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return upload_path


@app.get("/api/health")
def health():
    return {
        "app": "FreezeFont",
        "status": "running",
    }


@app.post("/inspect")
async def inspect_uploaded_font(file: UploadFile = File(...)):
    upload_path = save_upload(file)

    try:
        return inspect_font(str(upload_path))
    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail=f"Unable to inspect this font: {exc}",
        ) from exc


@app.post("/upload")
async def upload_font(
    file: UploadFile = File(...),
    mode: str = Form("all"),
    selected_styles: str = Form("[]"),
):
    upload_path = save_upload(file)
    job_output_folder = OUTPUT_FOLDER / uuid4().hex

    try:
        selected_styles_list = json.loads(selected_styles)
        if not isinstance(selected_styles_list, list):
            selected_styles_list = []
    except json.JSONDecodeError:
        selected_styles_list = []

    try:
        zip_path = freeze_font(
            str(upload_path),
            str(job_output_folder),
            mode,
            selected_styles_list,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail=f"Unable to convert this font: {exc}",
        ) from exc

    return FileResponse(
        path=zip_path,
        filename=Path(zip_path).name,
        media_type="application/zip",
    )


if FRONTEND_DIR.exists():
    app.mount(
        "/",
        StaticFiles(directory=str(FRONTEND_DIR), html=True),
        name="frontend",
    )
