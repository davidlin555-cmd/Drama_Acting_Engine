import logging
import random

# Configure logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def evaluate_video(video_path: str):
    """
    Mock function to simulate visual model scoring logic.
    Inputs:
        video_path (str): The path to the video to be evaluated.
    Outputs:
        score (int): A score from 0 to 100.
        reason (str): Error reason if any.
    """
    logger.info(f"Evaluator: Inspecting video at '{video_path}' for facial distortion and quality.")

    # Mocking a random score and reason
    score = random.randint(50, 100)

    if score >= 80:
        reason = "Quality is good. No significant distortion detected."
        logger.info(f"Evaluator: Video passed with score {score}.")
    else:
        reasons = [
            "Severe facial distortion detected in keyframes.",
            "Inconsistent lighting on face.",
            "Unnatural micro-expressions.",
            "Lip sync issues detected."
        ]
        reason = random.choice(reasons)
        logger.warning(f"Evaluator: Video failed with score {score}. Reason: {reason}")

    return {"score": score, "reason": reason}
