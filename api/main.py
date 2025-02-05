from fastapi import FastAPI
import uvicorn
from api.routes import router as api_router
from api.db import setup_indexes


app = FastAPI(
    title="Medalists API",
    description="API for uploading and aggregating medalist data",
    version="1.0.0"
)

# Include API routes
app.include_router(api_router)

# MongoDB: Set up indexes on startup
@app.on_event("startup")
async def startup_event():
    await setup_indexes()

# Run the FastAPI server
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
