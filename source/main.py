from fastapi import FastAPI, UploadFile, File
from typing import Dict

app = FastAPI(
    title="File transformation API test",
    version="0.1.0",
    description="Short demonstration to receive a ZIP and process it."
)

@app.get("/", tags=["Health Check"])
async def read_root() -> Dict[str, str]:
    """
    Endpoint to see the application's healthy
    """
    return {"status": "ok", "message": "It's running"}

@app.post("/upload/", tags=["File Processing"])
async def create_upload_file(file: UploadFile = File(...)) -> Dict[str, str]:
    """
    Endpoint to upload zip files
    """

    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "message": "File received!"
    }