"""
Fingerprint matching by comparing minutiae sets.
Uses simple distance + angle consistency (no full alignment for simplicity).
Suitable for same-finger images with similar scale/rotation.
"""
import numpy as np
from typing import List, Tuple
from .minutiae import Minutia, minutiae_to_vectors


def match_fingerprints(
    minutiae1: List[Minutia],
    minutiae2: List[Minutia],
    distance_threshold: float = 12.0,
    angle_threshold: float = 0.5,
    min_matches: int = 6,
) -> Tuple[bool, float, int]:
    """
    Compare two minutiae sets. Returns (matched, score, num_matching_pairs).
    score in [0,1]; matched = True if score >= typical threshold (e.g. 0.35).
    """
    if not minutiae1 or not minutiae2:
        return False, 0.0, 0

    V1 = minutiae_to_vectors(minutiae1)
    V2 = minutiae_to_vectors(minutiae2)
    n1, n2 = len(V1), len(V2)
    # Score as fraction of max possible matches over min(n1,n2)
    max_possible = min(n1, n2)
    matches = _count_matching_pairs(
        V1, V2, distance_threshold, angle_threshold
    )
    score = matches / max_possible if max_possible > 0 else 0.0
    matched = score >= 0.35 and matches >= min_matches
    return matched, float(score), matches


def _count_matching_pairs(
    V1: np.ndarray,
    V2: np.ndarray,
    dist_thresh: float,
    angle_thresh: float,
) -> int:
    """Count pairs (i in V1, j in V2) such that distance and angle are within threshold."""
    if V1.size == 0 or V2.size == 0:
        return 0
    count = 0
    # V columns: x, y, cos(a), sin(a), type_id
    for i in range(len(V1)):
        x1, y1, c1, s1, t1 = V1[i]
        for j in range(len(V2)):
            x2, y2, c2, s2, t2 = V2[j]
            if abs(t1 - t2) > 0.5:  # type must agree
                continue
            d = np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
            if d > dist_thresh:
                continue
            # Angle difference (cos/sin)
            angle_sim = c1 * c2 + s1 * s2
            if angle_sim >= (1 - angle_thresh):
                count += 1
                break  # one match per V1 point
    return count
