import logging
import shutil
import os
import time
from evaluator.vision_check import evaluate_video

# Configure logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def mock_render(source_image: str, driving_video: str, params: dict) -> str:
    """
    Mock function to simulate the core rendering of LivePortrait.
    """
    logger.info(f"Rendering video with params: {params}")
    # Simulating rendering time
    time.sleep(1)

    # Simulating saving output
    temp_output_path = "temp_output.mp4"
    # Create a dummy file
    with open(temp_output_path, "w") as f:
        f.write("dummy video data")

    logger.info(f"Rendering complete. Output saved to {temp_output_path}")
    return temp_output_path

def run_with_self_correction(source_image: str, driving_video: str) -> dict:
    """
    Executes the rendering process with a self-correction loop.
    Retries up to 3 times if the evaluator score is < 80.
    """
    max_retries = 3
    attempt = 0

    # Generic placeholder parameters to toggle
    params = {
        "relative": True,
        "paste_back": True,
        "expression_scale": 1.0
    }

    while attempt < max_retries:
        logger.info(f"Attempt {attempt + 1}/{max_retries} to render video.")

        try:
            temp_output = mock_render(source_image, driving_video, params)

            # Evaluator checking
            eval_result = evaluate_video(temp_output)
            score = eval_result["score"]
            reason = eval_result["reason"]

            if score >= 80:
                logger.info(f"Success! Video passed evaluation with score {score}.")
                return {"status": "success", "video_path": temp_output, "score": score}
            else:
                logger.warning(f"Evaluation failed (Score: {score}). Reason: {reason}. Triggering self-correction.")
                attempt += 1

                # Modify parameters for the next retry (self-correction logic)
                if attempt == 1:
                    params["relative"] = False
                    logger.info("Healer: Toggled 'relative' parameter to False.")
                elif attempt == 2:
                    params["paste_back"] = False
                    logger.info("Healer: Toggled 'paste_back' parameter to False.")

        except Exception as e:
            logger.error(f"Error during rendering or evaluation on attempt {attempt + 1}: {e}")
            attempt += 1

    # If it fails 3 times
    logger.error("Failed 3 times. Saving to hard_cases directory for further analysis.")
    try:
        os.makedirs("hard_cases", exist_ok=True)
        # Create dummy source files if they don't exist for the sake of the mock
        if not os.path.exists(source_image):
            with open(source_image, "w") as f: f.write("dummy image")
        if not os.path.exists(driving_video):
            with open(driving_video, "w") as f: f.write("dummy video")

        base_name = f"failed_case_{int(time.time())}"
        shutil.copy(source_image, os.path.join("hard_cases", f"{base_name}_img.png"))
        shutil.copy(driving_video, os.path.join("hard_cases", f"{base_name}_video.mp4"))
        logger.info(f"Copied source files to hard_cases as {base_name}")
    except Exception as e:
        logger.error(f"Failed to copy files to hard_cases: {e}")

    # Use a default score of None in case it was never set
    final_score = locals().get("score", None)
    return {"status": "failed", "reason": "Failed to generate acceptable video after 3 attempts.", "final_score": final_score}
