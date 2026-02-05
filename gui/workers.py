"""
Worker threads for enrollment and identification (keeps UI responsive).
"""
import os
from PyQt5.QtCore import QThread, pyqtSignal

# Import from parent package
import sys
_project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

import config
import main as biometric_main


class EnrollWorker(QThread):
    """Run enrollment in background."""
    progress = pyqtSignal(str)
    finished_success = pyqtSignal(object)  # db or (ids, features)
    finished_error = pyqtSignal(str)

    def __init__(self, mode: str, enroll_dir: str, parent=None):
        super().__init__(parent)
        self.mode = mode
        self.enroll_dir = enroll_dir
        self._cancelled = False

    def run(self):
        try:
            if self.mode == "fingerprint":
                self.progress.emit("Enrolling fingerprints...")
                db = biometric_main.enroll_fingerprints(self.enroll_dir)
                if not db:
                    self.finished_error.emit("No valid fingerprint images found in enrollment folder.")
                    return
                self.progress.emit(f"Enrolled {len(db)} identities: {', '.join(db.keys())}")
                self.finished_success.emit(db)
            else:
                self.progress.emit("Enrolling faces...")
                ids, features = biometric_main.enroll_faces(self.enroll_dir)
                if not ids:
                    self.finished_error.emit("No faces detected in enrollment folder.")
                    return
                self.progress.emit(f"Enrolled {len(ids)} face(s) from {len(set(ids))} identity(ies)")
                self.finished_success.emit((ids, features))
        except Exception as e:
            self.finished_error.emit(str(e))

    def cancel(self):
        self._cancelled = True


class IdentifyWorker(QThread):
    """Run identification in background."""
    progress = pyqtSignal(str)
    result_item = pyqtSignal(str, str)  # filename, identity
    finished_success = pyqtSignal(list)  # list of (path, identity)
    finished_error = pyqtSignal(str)

    def __init__(self, mode: str, query_paths: list, enrolled_data, parent=None):
        super().__init__(parent)
        self.mode = mode
        self.query_paths = query_paths
        self.enrolled_data = enrolled_data  # db for fingerprint, (ids, features) for face
        self._cancelled = False

    def run(self):
        try:
            results = []
            total = len(self.query_paths)
            for i, path in enumerate(self.query_paths):
                if self._cancelled:
                    break
                name = os.path.basename(path)
                self.progress.emit(f"Identifying {name} ({i+1}/{total})...")
                if self.mode == "fingerprint":
                    identity = biometric_main.identify_fingerprint(path, self.enrolled_data)
                else:
                    ids, features = self.enrolled_data
                    identity = biometric_main.identify_face(path, ids, features)
                results.append((path, identity))
                self.result_item.emit(name, identity)
            self.finished_success.emit(results)
        except Exception as e:
            self.finished_error.emit(str(e))

    def cancel(self):
        self._cancelled = True


class GenerateSamplesWorker(QThread):
    """Generate sample fingerprint images."""
    progress = pyqtSignal(str)
    finished_success = pyqtSignal()
    finished_error = pyqtSignal(str)

    def run(self):
        try:
            self.progress.emit("Generating sample fingerprints...")
            if _project_root not in sys.path:
                sys.path.insert(0, _project_root)
            import scripts.generate_sample_fingerprints as gen
            gen.main()
            self.progress.emit("Sample data created in data/fingerprints/")
            self.finished_success.emit()
        except Exception as e:
            self.finished_error.emit(str(e))
