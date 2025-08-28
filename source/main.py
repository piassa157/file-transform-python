from fastapi import FastAPI, UploadFile, File, HTTPException
from typing import Dict
import os
import shutil
from datetime import datetime
from pathlib import Path

from tasks import process_zip_file
from pydantic import BaseModel


class ReponseMessage(BaseModel):
    message: str
    task_queued: bool


app = FastAPI(
    title="File transformation API test",
    version="0.1.0",
    description="Short demonstration to receive a ZIP and process it."
)



STORAGE_PATH = Path("storage")
STORAGE_PATH.mkdir(exist_ok=True)

@app.get("/", tags=["Health Check"])
async def read_root() -> Dict[str, str]:
    """
    Endpoint to see the application's healthy
    """
    return {"status": "ok", "message": "It's running"}

@app.post("/upload/", tags=["File Processing"], response_model=ReponseMessage)
async def create_upload_file(file: UploadFile = File(...)) -> Dict[str, str]:
    """
    Endpoint to upload zip files
    """

    if not file.filename.endswith('.zip'):
        raise HTTPException(status_code=400,detail="File's format is wrong! It has accepted zip extensions")
    
    try:
        today_str = datetime.now().strftime("%m%d%Y")
        new_filename = f"{today_str}_{file.filename}"
        file_path = STORAGE_PATH / new_filename

        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        process_zip_file.delay(str(file_path))

        return {
            "message": "Finished",
            "task_queued": True
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"There was an error: {e}")