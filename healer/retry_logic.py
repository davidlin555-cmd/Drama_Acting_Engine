import logging
import shutil
import os
import time
from core.render import render_video
from evaluator.vision_check import evaluate_video

logger = logging.getLogger(__name__)

def process_with_self_correction(source_image: str, driving_video: str, max_retries: int = 3) -> str:
    """
    Implements the self-correcting while loop logic.
    """
    logger.info(f"Starting process_with_self_correction for {source_image} and {driving_video}")

    # Initial parameters
    relative = True
    paste_back = True

    attempts = 0
    while attempts < max_retries:
        logger.info(f"Attempt {attempts + 1}/{max_retries} with relative={relative}, paste_back={paste_back}")

        # 1. Render the video
        try:
            output_video_path = render_video(source_image, driving_video, relative, paste_back)
        except Exception as e:
            logger.error(f"Error during video rendering: {e}", exc_info=True)
            raise e

        # 2. Evaluate the video
        score, reason = evaluate_video(output_video_path)
        logger.info(f"Evaluation score: {score}, reason: {reason}")

        if score >= 80:
            logger.info(f"Video passed evaluation with score {score}.")
            return output_video_path

        # 3. Modify parameters for retry
        logger.warning(f"Video failed evaluation with score {score}. Adjusting parameters for retry.")

        # Simple adjustment logic based on AGENTS.md
        if attempts == 0:
            relative = False
            paste_back = True
        elif attempts == 1:
            relative = True
            paste_back = False
        elif attempts == 2:
             relative = False
             paste_back = False

        attempts += 1
        time.sleep(1) # Small delay for demonstration

    # If we exit the loop, it means we failed all retries
    logger.error(f"Failed to generate acceptable video after {max_retries} attempts.")

    # Copy to hard_cases directory
    hard_cases_dir = "hard_cases"
    os.makedirs(hard_cases_dir, exist_ok=True)

    timestamp = int(time.time())

    source_filename = os.path.basename(source_image) if source_image else "unknown_source.jpg"
    driving_filename = os.path.basename(driving_video) if driving_video else "unknown_driving.mp4"

    hard_case_source = os.path.join(hard_cases_dir, f"{timestamp}_{source_filename}")
    hard_case_driving = os.path.join(hard_cases_dir, f"{timestamp}_{driving_filename}")

    try:
        if os.path.exists(source_image):
            shutil.copy2(source_image, hard_case_source)
            logger.info(f"Copied source image to {hard_case_source}")
        else:
             logger.warning(f"Source image {source_image} not found, could not copy to hard_cases.")

        if os.path.exists(driving_video):
            shutil.copy2(driving_video, hard_case_driving)
            logger.info(f"Copied driving video to {hard_case_driving}")
        else:
             logger.warning(f"Driving video {driving_video} not found, could not copy to hard_cases.")
    except Exception as e:
        logger.error(f"Error copying files to hard_cases: {e}", exc_info=True)

    raise RuntimeError(f"Video generation failed after {max_retries} attempts. Hard cases saved.")
