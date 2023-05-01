# -*- coding:utf-8 -*-
import os
import shutil
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse

load_dotenv()

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

app = FastAPI()

static_path = Path(__file__).parent.absolute() / "../static"
file_dir = static_path / "uploads"
if not os.path.exists(file_dir):
    os.makedirs(file_dir)
download_dir = static_path / "download"
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

app.mount("/static", StaticFiles(directory=str(static_path), html=True), name="static")


@app.get("/")
async def read_root():
    return FileResponse("static/index.html")


@app.get("/admin")
async def read_admin_root():
    return FileResponse("static/admin.html")


@app.post("/upload")
async def upload_file(file: UploadFile):
    file_path = file_dir / file.filename
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    str().strip("fkjshadfasdfjs")
    return {"state": "OK", "filename": file.filename}
