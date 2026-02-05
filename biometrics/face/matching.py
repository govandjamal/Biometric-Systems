"""
Face matching by comparing feature vectors (from images, no webcam).
Uses cosine similarity or L2 distance.
"""
import numpy as np
from typing import List, Tuple, Optional


def match_faces(
    query_features: np.ndarray,
    enrolled_features: List[np.ndarray],
    enrolled_ids: List[str],
    threshold: float = 0.6,
    use_cosine: bool = True,
) -> Tuple[Optional[str], float]:
    """
    Find best matching enrolled identity.
    Returns (best_id, similarity). best_id is None if below threshold.
    """
    if query_features.size == 0 or not enrolled_features or not enrolled_ids:
        return None, 0.0
    if len(enrolled_features) != len(enrolled_ids):
        return None, 0.0

    best_id = None
    best_sim = -1.0
    for feat, uid in zip(enrolled_features, enrolled_ids):
        if feat.size == 0:
            continue
        if use_cosine:
            sim = _cosine_similarity(query_features, feat)
        else:
            sim = 1.0 / (1.0 + np.linalg.norm(query_features - feat))
        if sim > best_sim:
            best_sim = sim
            best_id = uid
    if best_sim < threshold:
        return None, best_sim
    return best_id, best_sim


def _cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """Cosine similarity in [0, 1] (assuming non-negative features)."""
    an = np.linalg.norm(a)
    bn = np.linalg.norm(b)
    if an < 1e-9 or bn < 1e-9:
        return 0.0
    return float(np.dot(a, b) / (an * bn))
