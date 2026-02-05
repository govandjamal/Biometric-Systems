"""
Minutiae extraction from thinned (skeleton) fingerprint images.
Uses crossing-number method: ridge endings (CN=1) and bifurcations (CN=3).
"""
import numpy as np
from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class Minutia:
    """Single minutia point."""
    x: int
    y: int
    type: str  # "ending" or "bifurcation"
    angle: float  # orientation in radians (simplified: from neighborhood)


def extract_minutiae(thinned: np.ndarray, min_distance: int = 8) -> List[Minutia]:
    """
    Extract ridge endings and bifurcations from a thinned fingerprint image.
    thinned: binary image, 1 = ridge (skeleton), 0 = background.
    min_distance: minimum distance between two minutiae (reduces noise).
    """
    if thinned is None or thinned.size == 0:
        return []

    # Ensure binary
    ridge = (thinned > 0).astype(np.uint8)
    h, w = ridge.shape
    minutiae: List[Minutia] = []

    # 8-neighborhood offsets
    dy = [-1, -1, 0, 1, 1, 1, 0, -1]
    dx = [0, 1, 1, 1, 0, -1, -1, -1]

    for y in range(2, h - 2):
        for x in range(2, w - 2):
            if ridge[y, x] == 0:
                continue
            # Crossing number: sum of transitions 0->1 in 8-neighborhood
            cn = 0
            for i in range(8):
                ny, nx = y + dy[i], x + dx[i]
                nv = ridge[ny, nx]
                nv_next = ridge[y + dy[(i + 1) % 8], x + dx[(i + 1) % 8]]
                cn += abs(int(nv) - int(nv_next))
            cn //= 2

            if cn == 1:
                m_type = "ending"
            elif cn == 3:
                m_type = "bifurcation"
            else:
                continue

            angle = _estimate_angle(ridge, x, y, dx, dy)
            minutiae.append(Minutia(x=x, y=y, type=m_type, angle=angle))

    # Remove minutiae too close to each other (keep first in list)
    minutiae = _filter_by_distance(minutiae, min_distance)
    return minutiae


def _estimate_angle(ridge: np.ndarray, x: int, y: int, dx: list, dy: list) -> float:
    """Rough orientation from 8-neighborhood (direction of ridge)."""
    # For ending: direction from neighbor toward this point
    # For bifurcation: use average of ridge directions (simplified: 0)
    neighbors = []
    for i in range(8):
        nx, ny = x + dx[i], y + dy[i]
        if 0 <= ny < ridge.shape[0] and 0 <= nx < ridge.shape[1] and ridge[ny, nx] > 0:
            # Vector from (nx,ny) to (x,y)
            neighbors.append((x - nx, y - ny))
    if not neighbors:
        return 0.0
    ax = sum(v[0] for v in neighbors) / len(neighbors)
    ay = sum(v[1] for v in neighbors) / len(neighbors)
    return np.arctan2(-ay, ax)


def _filter_by_distance(minutiae: List[Minutia], min_dist: int) -> List[Minutia]:
    """Keep only minutiae that are at least min_dist apart."""
    if min_dist <= 0 or not minutiae:
        return minutiae
    kept: List[Minutia] = []
    for m in minutiae:
        too_close = False
        for k in kept:
            d = np.sqrt((m.x - k.x) ** 2 + (m.y - k.y) ** 2)
            if d < min_dist:
                too_close = True
                break
        if not too_close:
            kept.append(m)
    return kept


def minutiae_to_vectors(minutiae: List[Minutia]) -> np.ndarray:
    """Convert list of Minutia to matrix [x, y, cos(angle), sin(angle), type_id] for matching."""
    if not minutiae:
        return np.zeros((0, 5))
    type_id = {"ending": 0, "bifurcation": 1}
    rows = []
    for m in minutiae:
        rows.append([m.x, m.y, np.cos(m.angle), np.sin(m.angle), type_id.get(m.type, 0)])
    return np.array(rows, dtype=np.float64)
