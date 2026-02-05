"""
Generate synthetic fingerprint-like images for testing (no hardware/dataset needed).
Creates ridge patterns and saves to data/fingerprints/enrolled and query.
"""
import os
import numpy as np
import cv2

# Project root
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
DATA = os.path.join(PROJECT_ROOT, "data", "fingerprints")
ENROLL = os.path.join(DATA, "enrolled")
QUERY = os.path.join(DATA, "query")


def make_ridge_image(shape=(256, 256), freq=0.04, angle=0.0, phase=0.0, noise=0.05):
    """Synthetic ridge pattern: sinusoidal waves + noise."""
    h, w = shape
    y, x = np.ogrid[:h, :w]
    # Orientation
    c, s = np.cos(angle), np.sin(angle)
    u = x * c + y * s
    g = np.sin(2 * np.pi * freq * u + phase) > 0
    g = (g.astype(np.float32) + np.random.rand(h, w).astype(np.float32) * noise)
    g = np.clip(g, 0, 1)
    # Slight blur to mimic skin
    g = cv2.GaussianBlur(g, (3, 3), 0.5)
    return (g * 255).astype(np.uint8)


def main():
    os.makedirs(ENROLL, exist_ok=True)
    os.makedirs(QUERY, exist_ok=True)

    # Person 1: two enrolled samples, one query
    for i in range(2):
        img = make_ridge_image(angle=0.2, phase=i * 0.7)
        path = os.path.join(ENROLL, "person_01", f"sample_{i+1}.png")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        cv2.imwrite(path, img)
    img = make_ridge_image(angle=0.25, phase=0.3)  # same person, slight variation
    cv2.imwrite(os.path.join(QUERY, "query_p1.png"), img)

    # Person 2: one enrolled, one query
    img = make_ridge_image(angle=-0.3, freq=0.05, phase=0.0)
    path = os.path.join(ENROLL, "person_02", "sample_1.png")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    cv2.imwrite(path, img)
    img = make_ridge_image(angle=-0.28, freq=0.05, phase=0.5)
    cv2.imwrite(os.path.join(QUERY, "query_p2.png"), img)

    # Unknown: query that does not match (different freq/angle)
    img = make_ridge_image(angle=1.2, freq=0.08, phase=0.0)
    cv2.imwrite(os.path.join(QUERY, "query_unknown.png"), img)

    print("Sample fingerprint images generated:")
    print("  Enrolled: data/fingerprints/enrolled/person_01/, person_02/")
    print("  Query:    data/fingerprints/query/query_p1.png, query_p2.png, query_unknown.png")
    print("Run: python main.py --mode fingerprint")


if __name__ == "__main__":
    main()
