"""
Face feature extraction from cropped face images (no webcam).
Uses LBP (Local Binary Pattern) histogram as compact descriptor;
alternative: resized grayscale patch. All from image arrays.
"""
import cv2
import numpy as np
from typing import Optional, List


def extract_face_features(
    image: np.ndarray,
    face_rect: Optional[tuple] = None,
    size: tuple = (64, 64),
    use_lbp: bool = True,
) -> np.ndarray:
    """
    Extract feature vector from face image.
    image: full image (BGR or gray). If face_rect (x,y,w,h) given, crop first.
    size: resize face to this for consistent feature length.
    use_lbp: if True, LBP histogram; else flattened grayscale patch.
    """
    if image is None or image.size == 0:
        return np.array([])
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image.copy()
    if face_rect is not None:
        x, y, w, h = face_rect
        gray = gray[y : y + h, x : x + w]
    face = cv2.resize(gray, size, interpolation=cv2.INTER_AREA)
    if use_lbp:
        return _lbp_histogram(face)
    return face.astype(np.float32).flatten() / 255.0


def _lbp_histogram(patch: np.ndarray, num_points: int = 8, radius: int = 1) -> np.ndarray:
    """LBP histogram (256 bins for 8-neighbor LBP codes)."""
    lbp = _local_binary_pattern(patch, num_points, radius)
    n_bins = 256
    hist, _ = np.histogram(lbp.ravel(), bins=n_bins, range=(0, n_bins), density=True)
    return hist.astype(np.float32)


def _local_binary_pattern(img: np.ndarray, num_points: int, radius: int) -> np.ndarray:
    """Basic 3x3 LBP: compare center with 8 neighbors."""
    h, w = img.shape
    out = np.zeros_like(img, dtype=np.uint8)
    for i in range(1, h - 1):
        for j in range(1, w - 1):
            center = img[i, j]
            code = 0
            code |= (1 << 0) if img[i - 1, j] >= center else 0
            code |= (1 << 1) if img[i - 1, j + 1] >= center else 0
            code |= (1 << 2) if img[i, j + 1] >= center else 0
            code |= (1 << 3) if img[i + 1, j + 1] >= center else 0
            code |= (1 << 4) if img[i + 1, j] >= center else 0
            code |= (1 << 5) if img[i + 1, j - 1] >= center else 0
            code |= (1 << 6) if img[i, j - 1] >= center else 0
            code |= (1 << 7) if img[i - 1, j - 1] >= center else 0
            out[i, j] = code
    return out
