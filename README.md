# FreezeFont

FreezeFont is a small web app for inspecting variable fonts and exporting their named instances as static `.ttf` files.

## Features

- Upload TTF, OTF, WOFF, or WOFF2 variable fonts
- Inspect font family, axes, and named instances before conversion
- Convert recommended basic styles, every named style, or selected custom styles
- Download generated static fonts as a ZIP file
- Single FastAPI app serves both the API and frontend UI

## Tech Stack

- FastAPI
- FontTools
- Brotli
- Vanilla HTML, CSS, and JavaScript

## Run Locally

Create a virtual environment and install the locked dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-lock.txt
```

Start the web app:

```bash
uvicorn backend.app:app --host 127.0.0.1 --port 8000 --reload
```

Open the app in your browser:

```text
http://127.0.0.1:8000
```

Health check:

```text
http://127.0.0.1:8000/api/health
```

## API Endpoints

- `POST /inspect` — upload a font and receive metadata about variable axes and named instances.
- `POST /upload` — upload a font, choose a conversion mode, and receive a ZIP file.

`/upload` form fields:

- `file`: the variable font file
- `mode`: `basic`, `all`, or `selected`
- `selected_styles`: JSON array of named styles, used when `mode` is `selected`
