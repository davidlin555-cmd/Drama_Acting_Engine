import logging
import random
from typing import Tuple

logger = logging.getLogger(__name__)

def evaluate_video(video_path: str) -> Tuple[int, str]:
    """
    Mock function simulating a vision large model scoring logic.
    Returns a score from 0-100 and an error reason (if any).
    """
    logger.info(f"Evaluating video: {video_path}")

    # Simulate some logic to determine the score
    # For testing purposes, we can use a random score or define a specific behavior based on path
    score = random.randint(50, 100)

    # We can also use a deterministic way for testing if the path contains a specific keyword
    if "fail" in video_path.lower():
        score = 60
    elif "success" in video_path.lower():
        score = 90

    reason = "Video quality is good" if score >= 80 else "Face distortion detected"
    logger.info(f"Evaluation complete for {video_path}: Score={score}, Reason={reason}")
    return score, reason
