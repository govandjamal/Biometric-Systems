"""
Face detection from images (no webcam).
Uses OpenCV Haar cascade or DNN; loads image from file.
"""
import cv2
import numpy as np
from typing import Optional, Tuple, List

# Default cascade path (bundled with OpenCV)
CASCADE_PATH = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"


def load_detector():
    """Load default face detector."""
    return cv2.CascadeClassifier(CASCADE_PATH)


def detect_face(
    image: np.ndarray,
    detector: Optional[cv2.CascadeClassifier] = None,
    scale_factor: float = 1.1,
    min_neighbors: int = 5,
    min_size: Tuple[int, int] = (30, 30),
) -> List[Tuple[int, int, int, int]]:
    """
    Detect face(s) in image. Returns list of (x, y, w, h) rectangles.
    image: BGR or grayscale (e.g. from cv2.imread).
    """
    if image is None or image.size == 0:
        return []
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
    if detector is None:
        detector = load_detector()
    rects = detector.detectMultiScale(
        gray, scaleFactor=scale_factor, minNeighbors=min_neighbors, minSize=min_size
    )
    return [(int(x), int(y), int(w), int(h)) for (x, y, w, h) in rects]
