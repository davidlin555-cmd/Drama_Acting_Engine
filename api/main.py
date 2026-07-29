import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from healer.retry_logic import process_with_self_correction

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(title="Drama Acting Engine API")

class GenerateRequest(BaseModel):
    source_image: str
    driving_video: str

@app.post("/generate_acting")
def generate_acting(request: GenerateRequest):
    logger.info(f"Received request: source_image={request.source_image}, driving_video={request.driving_video}")
    try:
        result_path = process_with_self_correction(request.source_image, request.driving_video)
        logger.info(f"Successfully processed request. Result saved at: {result_path}")
        return {"status": "success", "video_path": result_path}
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
