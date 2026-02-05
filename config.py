"""
Configuration for the biometric module.
All paths are relative to project root. No webcam or hardware is used.
"""
import os

# Base directory for data (image files only)
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_ROOT = os.path.join(PROJECT_ROOT, "data")

# Fingerprint paths
FINGERPRINT_ENROLL_DIR = os.path.join(DATA_ROOT, "fingerprints", "enrolled")
FINGERPRINT_QUERY_DIR = os.path.join(DATA_ROOT, "fingerprints", "query")

# Face paths
FACE_ENROLL_DIR = os.path.join(DATA_ROOT, "faces", "enrolled")
FACE_QUERY_DIR = os.path.join(DATA_ROOT, "faces", "query")

# Fingerprint processing parameters
FINGERPRINT_RESIZE = (256, 256)  # Normalized size for processing
BLOCK_SIZE = 16
MINUTIAE_NEIGHBORHOOD = 3
MIN_MINUTIAE_DISTANCE = 8
MATCH_THRESHOLD = 0.35  # Min fraction of matching minutiae for positive ID

# Supported image extensions
IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff")
