import base64
import os
import uuid
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from openai import OpenAI

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR / "uploaded_image"
EDITED_DIR = BASE_DIR / "edited_image"

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
EDITED_DIR.mkdir(parents=True, exist_ok=True)

client = OpenAI()

app = FastAPI(title="Image Edit App API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/edited_image", StaticFiles(directory=EDITED_DIR), name="edited_image")


def edit_image_based_on_prompt(original_image: Path, prompt: str) -> Path:
    """Edit the given image using OpenAI's image editing model."""
    if not original_image.exists():
        raise FileNotFoundError("Original image not found")

    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY is not configured")

    try:
        with open(original_image, "rb") as image_file:
            result = client.images.edit(
                model="gpt-image-1-mini",
                image=[image_file],
                prompt=prompt,
            )
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError(f"OpenAI image edit failed: {exc}") from exc

    image_base64 = result.data[0].b64_json
    image_bytes = base64.b64decode(image_base64)

    output_filename = f"edited_{uuid.uuid4().hex}.png"
    output_path = EDITED_DIR / output_filename
    with open(output_path, "wb") as f:
        f.write(image_bytes)

    return output_path


@app.post("/api/edit")
async def edit_image(file: UploadFile = File(...), prompt: str = Form(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="File upload is required")
    if not prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt is required")

    saved_filename = f"upload_{uuid.uuid4().hex}_{file.filename}"
    saved_path = UPLOAD_DIR / saved_filename

    with open(saved_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)

    try:
        edited_path = edit_image_based_on_prompt(saved_path, prompt)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Original image not found")
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc))

    edited_url = f"/edited_image/{edited_path.name}"
    return JSONResponse({"edited_image_url": edited_url})


@app.get("/api/health")
async def health_check():
    return {"status": "ok"}
