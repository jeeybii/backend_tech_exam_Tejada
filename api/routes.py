from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import shutil
import os
from api.services import add_medalist, fetch_event_stats

# Define Router
router = APIRouter()

# Storage directory for uploaded CSVs
UPLOAD_FOLDER = "storage/app/medalists"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure folder exists

### 📌 1. File Upload Endpoint ###
@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """ Upload a CSV file to the storage directory. """
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed.")

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return JSONResponse(
            content={"message": "File uploaded successfully!", "file_name": file.filename},
            status_code=201
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")


### 📌 2. Fetch Aggregated Stats Endpoint ###
@router.get("/aggregated_stats/event")
async def get_event_stats(page: int = 1, limit: int = 10):
    """ Retrieve aggregated event statistics with pagination. """
    try:
        stats = await fetch_event_stats(page, limit)
        return JSONResponse(content=stats, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving stats: {str(e)}")
