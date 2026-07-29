from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging
from healer.retry_logic import run_with_self_correction

# Configure logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Drama Acting Engine API")

class GenerationRequest(BaseModel):
    source_image: str
    driving_video: str

@app.post("/generate_acting")
async def generate_acting(request: GenerationRequest):
    logger.info(f"Received request to generate acting: image='{request.source_image}', video='{request.driving_video}'")

    result = run_with_self_correction(request.source_image, request.driving_video)

    if result["status"] == "success":
        return {"message": "Video generated successfully", "data": result}
    else:
        raise HTTPException(status_code=500, detail=f"Generation failed: {result['reason']}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
