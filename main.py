import os
from typing import Union

from fastapi import FastAPI

from utils.logging import get_logger, setup_logging


setup_logging(
    log_level=os.getenv("LOG_LEVEL", "INFO"),
    json_format=os.getenv("JSON_LOG_FORMAT", "False").lower() == "true",
    log_file=os.getenv("LOG_FILE"),
)
logger = get_logger(__name__)

app = FastAPI()


@app.get("/")
async def root():
    """Return a simple health check message."""
    logger.info("Health check endpoint called")
    return {"message": "Hello World"}
