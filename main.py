"""
Biometric Module - Main entry point.
Runs fingerprint or face recognition using only image files (no webcam, no hardware).
"""
import os
import argparse
import cv2

import config
from biometrics.fingerprint import preprocess_fingerprint, extract_minutiae, match_fingerprints
from biometrics.face import detect_face, load_detector, extract_face_features, match_faces


def _collect_images(root: str) -> dict:
    """Collect image paths: { identity_id: [path1, path2, ...] }.
    If root contains subdirs, each subdir name = identity; else all images = one identity 'default'.
    """
    root = os.path.abspath(root)
    if not os.path.isdir(root):
        return {}
    result = {}
    for name in sorted(os.listdir(root)):
        path = os.path.join(root, name)
        if os.path.isdir(path):
            files = [
                os.path.join(path, f)
                for f in os.listdir(path)
                if f.lower().endswith(config.IMAGE_EXTENSIONS)
            ]
            if files:
                result[name] = files
        else:
            if name.lower().endswith(config.IMAGE_EXTENSIONS):
                result.setdefault("default", []).append(path)
    return result


def _load_image(path: str):
    img = cv2.imread(path)
    if img is None:
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    return img


# ---------- Fingerprint pipeline ----------


def enroll_fingerprints(enroll_dir: str) -> dict:
    """Enroll: load images per identity, preprocess, extract minutiae. Returns { id: [minutiae_list, ...] }."""
    identities = _collect_images(enroll_dir)
    db = {}
    for identity, paths in identities.items():
        minutiae_list = []
        for path in paths:
            img = _load_image(path)
            if img is None:
                continue
            try:
                thinned = preprocess_fingerprint(img, config.FINGERPRINT_RESIZE)
                minutiae = extract_minutiae(thinned, config.MIN_MINUTIAE_DISTANCE)
                minutiae_list.append(minutiae)
            except Exception as e:
                print(f"  Skip {path}: {e}")
        if minutiae_list:
            db[identity] = minutiae_list
    return db


def identify_fingerprint(query_path: str, db: dict) -> str:
    """Identify one query image against enrolled DB. Returns best matching identity or 'Unknown'."""
    img = _load_image(query_path)
    if img is None:
        return "Unknown"
    try:
        thinned = preprocess_fingerprint(img, config.FINGERPRINT_RESIZE)
        query_minutiae = extract_minutiae(thinned, config.MIN_MINUTIAE_DISTANCE)
    except Exception:
        return "Unknown"
    best_id = "Unknown"
    best_score = 0.0
    for identity, minutiae_list in db.items():
        for enrolled_min in minutiae_list:
            matched, score, _ = match_fingerprints(
                query_minutiae,
                enrolled_min,
                min_matches=4,
            )
            if score > best_score:
                best_score = score
                best_id = identity
    if best_score < config.MATCH_THRESHOLD:
        return "Unknown"
    return best_id


def run_fingerprint(enroll_dir: str, query_dir: str):
    print("Fingerprint module (image-based, no hardware)")
    print("Enrolling from:", enroll_dir)
    db = enroll_fingerprints(enroll_dir)
    if not db:
        print("No enrolled identities. Add images under", enroll_dir)
        print("  e.g. enrolled/person_01/img1.png, enrolled/person_02/img1.png")
        return
    print("Enrolled identities:", list(db.keys()))
    print("Query from:", query_dir)
    if not os.path.isdir(query_dir):
        os.makedirs(query_dir, exist_ok=True)
        print("  (query folder created; add fingerprint images and run again)")
        return
    for f in sorted(os.listdir(query_dir)):
        if not f.lower().endswith(config.IMAGE_EXTENSIONS):
            continue
        path = os.path.join(query_dir, f)
        identity = identify_fingerprint(path, db)
        print(f"  {f} -> {identity}")


# ---------- Face pipeline ----------


def enroll_faces(enroll_dir: str):
    """Enroll: load images per identity, detect face, extract features. Returns (ids, list of feature lists)."""
    identities = _collect_images(enroll_dir)
    detector = load_detector()
    ids = []
    all_features = []
    for identity, paths in identities.items():
        for path in paths:
            img = _load_image(path)
            if img is None:
                continue
            rects = detect_face(img, detector=detector)
            if not rects:
                continue
            # Use first face
            feat = extract_face_features(img, face_rect=rects[0])
            if feat.size > 0:
                ids.append(identity)
                all_features.append(feat)
    return ids, all_features


def identify_face(query_path: str, enrolled_ids: list, enrolled_features: list) -> str:
    img = _load_image(query_path)
    if img is None:
        return "Unknown"
    detector = load_detector()
    rects = detect_face(img, detector=detector)
    if not rects:
        return "Unknown"
    feat = extract_face_features(img, face_rect=rects[0])
    best_id, sim = match_faces(feat, enrolled_features, enrolled_ids, threshold=0.5)
    return best_id if best_id else "Unknown"


def run_face(enroll_dir: str, query_dir: str):
    print("Face module (image-based, no webcam)")
    print("Enrolling from:", enroll_dir)
    ids, features = enroll_faces(enroll_dir)
    if not ids:
        print("No faces enrolled. Add images (one folder per person) under", enroll_dir)
        return
    print("Enrolled:", len(ids), "faces from identities", list(set(ids)))
    print("Query from:", query_dir)
    if not os.path.isdir(query_dir):
        os.makedirs(query_dir, exist_ok=True)
        print("  (query folder created; add face images and run again)")
        return
    for f in sorted(os.listdir(query_dir)):
        if not f.lower().endswith(config.IMAGE_EXTENSIONS):
            continue
        path = os.path.join(query_dir, f)
        identity = identify_face(path, ids, features)
        print(f"  {f} -> {identity}")


# ---------- CLI ----------


def main():
    parser = argparse.ArgumentParser(
        description="Biometric module: fingerprint or face from image files (no webcam/hardware)."
    )
    parser.add_argument(
        "--mode",
        choices=["fingerprint", "face"],
        default="fingerprint",
        help="Biometric modality",
    )
    parser.add_argument("--enroll-dir", default=None, help="Enrollment images directory")
    parser.add_argument("--query-dir", default=None, help="Query images directory")
    args = parser.parse_args()

    if args.mode == "fingerprint":
        enroll = args.enroll_dir or config.FINGERPRINT_ENROLL_DIR
        query = args.query_dir or config.FINGERPRINT_QUERY_DIR
        run_fingerprint(enroll, query)
    else:
        enroll = args.enroll_dir or config.FACE_ENROLL_DIR
        query = args.query_dir or config.FACE_QUERY_DIR
        run_face(enroll, query)


if __name__ == "__main__":
    main()
