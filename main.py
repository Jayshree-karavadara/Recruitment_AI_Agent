import os
import sys
from pathlib import Path
import logging

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from fastapi import FastAPI, Request, Response
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Import local modules
from src.api import routes
from src.utils.logger import get_logger

# Initialize logger
logger = get_logger(__name__)

app = FastAPI(
    title="Recruitment AI Agent",
    description="A web application for ranking candidates based on their resumes and a job description.",
    version="0.2.0",  # Version incremented to reflect refactoring
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this to your frontend's domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Centralized Exception Handler ---
@app.exception_handler(Exception)
async def handle_generic_exception(request: Request, exc: Exception):
    """
    Handles any unhandled exception in the application, logs it,
    and returns a standardized 500 Internal Server Error JSON response.
    """
    logger.error(f"Unhandled exception for request {request.method} {request.url}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected internal server error occurred."},
    )

# Determine the base directory to correctly locate the 'static' and 'templates' folders
# Set base directory to the project root
base_dir = Path(__file__).resolve().parent

# Mount the static files directory
app.mount("/static", StaticFiles(directory=base_dir / "static"), name="static")

# Include the API router
app.include_router(routes.router)



# --- Entry point ---
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",          # module_name:variable_name
        host="127.0.0.1",      # accessible from other devices
        port=8000,           # default port
        reload=True          # auto-reload on code changes
    )
