# FreezeFont

FreezeFont is a ready-to-use web app for inspecting variable fonts and exporting their named instances as static `.ttf` files.

## What it does

- Upload TTF, OTF, WOFF, or WOFF2 variable fonts
- Inspect font family, variable axes, and named instances before conversion
- Convert recommended basic styles, every named style, or selected custom styles
- Download generated static fonts as a ZIP file
- Run as one FastAPI website: the backend API also serves the frontend UI

## Tech Stack

- FastAPI
- FontTools
- Brotli
- Vanilla HTML, CSS, and JavaScript

## Quick Start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
./start.sh
```

Open:

```text
http://127.0.0.1:8000
```

## Alternative Local Run

```bash
uvicorn backend.app:app --host 127.0.0.1 --port 8000 --reload
```

## Docker Run

```bash
docker build -t freezefont .
docker run --rm -p 8000:8000 freezefont
```

Open:

```text
http://127.0.0.1:8000
```

## Deploy

FreezeFont is ready for common Python/Docker hosting platforms.

### Render / Railway / Heroku-style

Use the included `Procfile`:

```text
web: uvicorn backend.app:app --host 0.0.0.0 --port ${PORT:-8000}
```

### Docker platforms

Use the included `Dockerfile`. The container listens on `$PORT`, defaulting to `8000`.

## API Endpoints

- `GET /api/health` — health check
- `POST /inspect` — upload a font and receive metadata about variable axes and named instances
- `POST /upload` — upload a font, choose a conversion mode, and receive a ZIP file

`/upload` form fields:

- `file`: the variable font file
- `mode`: `basic`, `all`, or `selected`
- `selected_styles`: JSON array of named styles, used when `mode` is `selected`

## Project Structure

```text
backend/        FastAPI app and font conversion services
fontend/        Static website UI served by FastAPI
uploads/        Existing sample uploads plus ignored runtime uploads
output/         Existing sample outputs plus ignored runtime outputs
```
