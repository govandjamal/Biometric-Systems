"""
Fingerprint preprocessing pipeline.
Works on images loaded from disk (no hardware).
"""
import cv2
import numpy as np
from skimage.morphology import skeletonize


def preprocess_fingerprint(image: np.ndarray, target_size=(256, 256)) -> np.ndarray:
    """
    Full preprocessing: normalize, enhance, binarize, thin (skeletonize).
    Input: BGR or grayscale image (e.g. from cv2.imread).
    Output: binary thinned image (skeleton) for minutiae extraction.
    """
    if image is None or image.size == 0:
        raise ValueError("Empty image")

    # Grayscale
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image.copy()

    # Resize for consistent processing
    gray = cv2.resize(gray, target_size, interpolation=cv2.INTER_AREA)

    # Normalize
    normalized = _normalize(gray)

    # Enhance: CLAHE to improve contrast in ridge regions
    enhanced = _enhance(normalized)

    # Binarize
    binary = _binarize(enhanced)

    # Thinning (skeletonization) for minutiae extraction
    thinned = _thin(binary)

    return thinned.astype(np.uint8)


def _normalize(img: np.ndarray) -> np.ndarray:
    """Normalize to zero mean and unit variance (or fixed range)."""
    mean = np.mean(img)
    std = np.std(img)
    if std < 1e-6:
        return img
    out = (img.astype(np.float64) - mean) / std
    out = np.clip(out * 32 + 128, 0, 255).astype(np.uint8)
    return out


def _enhance(img: np.ndarray) -> np.ndarray:
    """Contrast enhancement using CLAHE."""
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    return clahe.apply(img)


def _binarize(img: np.ndarray) -> np.ndarray:
    """Adaptive binarization; ridges become 1 (white) or 0 (black) depending on convention.
    We use Otsu when possible, else adaptive threshold. Output: 0 = background, 1 = ridge.
    """
    # Otsu for global threshold
    _, binary = cv2.threshold(img, 0, 1, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # Ensure ridges are 1 (white) - fingerprint images often have dark ridges
    if np.sum(binary) > binary.size // 2:
        binary = 1 - binary
    return binary.astype(np.uint8)


def _thin(binary: np.ndarray) -> np.ndarray:
    """Morphological thinning (skeletonization). Ridge pixels = 1."""
    # skeletonize expects 0 = background, non-zero = foreground
    skeleton = skeletonize(binary.astype(bool)).astype(np.uint8)
    return skeleton
