"""
Main application window for Biometric Systems.
"""
import os
import re
import shutil
from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
    QLabel,
    QLineEdit,
    QPushButton,
    QListWidget,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QTabWidget,
    QFileDialog,
    QMessageBox,
    QProgressBar,
    QSplitter,
    QFrame,
    QMenuBar,
    QMenu,
    QAction,
    QStatusBar,
    QHeaderView,
    QAbstractItemView,
    QApplication,
    QGridLayout,
    QSizePolicy,
    QScrollArea,
    QInputDialog,
)
from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtGui import QFont, QPixmap, QImage

import sys
_project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)
import config

from .styles import STYLESHEET
from .workers import EnrollWorker, IdentifyWorker, GenerateSamplesWorker


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Biometric Systems — Fingerprint & Face (Image-based)")
        self.setMinimumSize(940, 860)
        self.resize(1100, 900)
        self.setStyleSheet(STYLESHEET)

        # State: enrolled data per mode
        self.fingerprint_db = None
        self.face_ids = []
        self.face_features = []
        self._enroll_worker = None
        self._identify_worker = None
        self._samples_worker = None

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(12)
        layout.setContentsMargins(16, 16, 16, 16)

        # Mode tabs (in splitter so content can use space)
        self.tabs = QTabWidget()
        self.tab_fingerprint = QWidget()
        self.tab_face = QWidget()
        self.tabs.addTab(self.tab_fingerprint, "Fingerprint")
        self.tabs.addTab(self.tab_face, "Face")
        self._build_fingerprint_tab()
        self._build_face_tab()

        # Log area - fixed height so it doesn't steal space
        log_group = QGroupBox("Log")
        log_layout = QVBoxLayout(log_group)
        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setMinimumHeight(80)
        self.log.setMaximumHeight(180)
        self.log.setPlaceholderText("Operations and results will appear here...")
        self.log.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        log_layout.addWidget(self.log)

        # Splitter: tabs get most space, log stays visible
        splitter = QSplitter(Qt.Vertical)
        splitter.addWidget(self.tabs)
        splitter.addWidget(log_group)
        splitter.setSizes([640, 180])  # tabs height, log height
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 0)
        layout.addWidget(splitter)

        # Progress bar (hidden until used)
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        # Footer
        footer = QFrame()
        footer.setObjectName("footer")
        footer_layout = QHBoxLayout(footer)
        footer_layout.setContentsMargins(0, 8, 0, 4)
        footer_label = QLabel("Kofand Saedd metrocola 2239066")
        footer_label.setObjectName("footerLabel")
        footer_layout.addWidget(footer_label, 0, Qt.AlignCenter)
        layout.addWidget(footer)

        self._add_menu_and_status()
        self._log("Application started. Loading saved enrollment from disk...")
        # Load any previously enrolled people from disk (so data is not lost after restart)
        QTimer.singleShot(400, self._auto_load_enrollment)

    def _build_fingerprint_tab(self):
        # Content widget that will go inside the scroll area
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(14)

        # --- Simple: Add person (one photo + name, app does the rest) ---
        easy_gb = QGroupBox("Add person (easy)")
        easy_gb.setMinimumHeight(100)
        easy_layout = QVBoxLayout(easy_gb)
        easy_layout.addWidget(QLabel("Choose a photo, then enter the person's name. The app will create folders and enroll automatically."))
        self.fp_add_person_btn = QPushButton("Add person — choose photo and enter name")
        self.fp_add_person_btn.setObjectName("primaryButton")
        self.fp_add_person_btn.setMinimumHeight(40)
        self.fp_add_person_btn.clicked.connect(lambda: self._add_person_from_photo("fingerprint"))
        easy_layout.addWidget(self.fp_add_person_btn)
        layout.addWidget(easy_gb)

        # Enrollment (auto-managed; list of enrolled people)
        enroll_gb = QGroupBox("Enrolled people")
        enroll_gb.setMinimumHeight(220)
        enroll_layout = QGridLayout(enroll_gb)
        enroll_layout.addWidget(QLabel("Enrollment folder:"), 0, 0)
        self.fp_enroll_path = QLineEdit()
        self.fp_enroll_path.setPlaceholderText("Folder with subfolders per person (e.g. person_01, person_02)")
        self.fp_enroll_path.setText(config.FINGERPRINT_ENROLL_DIR)
        self.fp_enroll_path.setMinimumWidth(240)
        self.fp_enroll_path.textChanged.connect(lambda t: self.fp_enroll_path.setToolTip(t))
        self.fp_enroll_path.setToolTip(self.fp_enroll_path.text())
        enroll_layout.addWidget(self.fp_enroll_path, 0, 1)
        enroll_layout.setColumnStretch(1, 1)
        self.fp_browse_enroll = QPushButton("Browse...")
        self.fp_browse_enroll.clicked.connect(lambda: self._browse_enroll("fingerprint"))
        enroll_layout.addWidget(self.fp_browse_enroll, 0, 2)
        self.fp_enroll_btn = QPushButton("Enroll")
        self.fp_enroll_btn.setObjectName("primaryButton")
        self.fp_enroll_btn.setMinimumHeight(36)
        self.fp_enroll_btn.clicked.connect(lambda: self._run_enroll("fingerprint"))
        enroll_layout.addWidget(self.fp_enroll_btn, 1, 1, 1, 2)
        self.fp_enrolled_list = QListWidget()
        self.fp_enrolled_list.setMinimumHeight(90)
        self.fp_enrolled_list.setMaximumHeight(200)
        self.fp_enrolled_list.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        enroll_layout.addWidget(QLabel("Enrolled identities:"), 2, 0)
        enroll_layout.addWidget(self.fp_enrolled_list, 3, 0, 1, 3)
        layout.addWidget(enroll_gb)

        # --- Identify: select one photo, then Identify ---
        query_gb = QGroupBox("Identify")
        query_gb.setMinimumHeight(180)
        query_layout = QGridLayout(query_gb)
        query_layout.addWidget(QLabel("Select a photo to identify, then click Identify."), 0, 0, 1, 3)
        sel_identify_btn = QPushButton("Select photo to identify")
        sel_identify_btn.setMinimumHeight(40)
        sel_identify_btn.clicked.connect(lambda: self._select_photo_to_identify("fingerprint"))
        query_layout.addWidget(sel_identify_btn, 1, 0, 1, 2)
        self.fp_query_path = QLineEdit()
        self.fp_query_path.setPlaceholderText("No photo selected — click the button above")
        self.fp_query_path.setReadOnly(True)
        self.fp_query_path.setMinimumWidth(240)
        self.fp_query_path.setMinimumHeight(36)
        self.fp_query_path.setText("")
        self.fp_query_path.textChanged.connect(lambda t: self.fp_query_path.setToolTip(t or "No photo selected"))
        query_layout.addWidget(self.fp_query_path, 2, 0)
        query_layout.setColumnStretch(0, 1)
        self.fp_browse_query = QPushButton("Browse...")
        self.fp_browse_query.setMinimumHeight(36)
        self.fp_browse_query.clicked.connect(lambda: self._browse_query("fingerprint"))
        query_layout.addWidget(self.fp_browse_query, 2, 1)
        self.fp_identify_btn = QPushButton("Identify")
        self.fp_identify_btn.setObjectName("primaryButton")
        self.fp_identify_btn.setMinimumHeight(40)
        self.fp_identify_btn.clicked.connect(lambda: self._run_identify("fingerprint"))
        query_layout.addWidget(self.fp_identify_btn, 3, 0, 1, 2)
        layout.addWidget(query_gb)

        # Preview
        preview_gb = QGroupBox("Preview")
        preview_layout = QVBoxLayout(preview_gb)
        self.fp_preview = QLabel()
        self.fp_preview.setAlignment(Qt.AlignCenter)
        self.fp_preview.setMinimumHeight(140)
        self.fp_preview.setMaximumHeight(200)
        self.fp_preview.setObjectName("previewLabel")
        self.fp_preview.setText("No image selected")
        preview_layout.addWidget(self.fp_preview)
        layout.addWidget(preview_gb)

        # Results table - scrollable, minimum height so rows are visible
        results_label = QLabel("Results:")
        layout.addWidget(results_label)
        self.fp_results = QTableWidget()
        self.fp_results.setColumnCount(2)
        self.fp_results.setHorizontalHeaderLabels(["Image", "Identity"])
        self.fp_results.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.fp_results.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.fp_results.setMinimumHeight(180)
        self.fp_results.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.fp_results.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.fp_results.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(self.fp_results, 1)

        # Put content in scroll area
        scroll = QScrollArea()
        scroll.setWidget(content)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setObjectName("tabScrollArea")
        tab_layout = QVBoxLayout(self.tab_fingerprint)
        tab_layout.setContentsMargins(0, 0, 0, 0)
        tab_layout.addWidget(scroll)

    def _build_face_tab(self):
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(14)

        # --- Simple: Add person (one photo + name) ---
        easy_gb_face = QGroupBox("Add person (easy)")
        easy_gb_face.setMinimumHeight(100)
        easy_layout_face = QVBoxLayout(easy_gb_face)
        easy_layout_face.addWidget(QLabel("Choose a photo, then enter the person's name. The app will create folders and enroll automatically."))
        self.face_add_person_btn = QPushButton("Add person — choose photo and enter name")
        self.face_add_person_btn.setObjectName("primaryButton")
        self.face_add_person_btn.setMinimumHeight(40)
        self.face_add_person_btn.clicked.connect(lambda: self._add_person_from_photo("face"))
        easy_layout_face.addWidget(self.face_add_person_btn)
        layout.addWidget(easy_gb_face)

        enroll_gb = QGroupBox("Enrolled people")
        enroll_gb.setMinimumHeight(220)
        enroll_layout = QGridLayout(enroll_gb)
        enroll_layout.addWidget(QLabel("Enrollment folder:"), 0, 0)
        self.face_enroll_path = QLineEdit()
        self.face_enroll_path.setPlaceholderText("(Managed automatically)")
        self.face_enroll_path.setText(config.FACE_ENROLL_DIR)
        self.face_enroll_path.setMinimumWidth(240)
        self.face_enroll_path.setReadOnly(True)
        self.face_enroll_path.textChanged.connect(lambda t: self.face_enroll_path.setToolTip(t or ""))
        enroll_layout.addWidget(self.face_enroll_path, 0, 1)
        enroll_layout.setColumnStretch(1, 1)
        self.face_browse_enroll = QPushButton("Browse...")
        self.face_browse_enroll.clicked.connect(lambda: self._browse_enroll("face"))
        enroll_layout.addWidget(self.face_browse_enroll, 0, 2)
        self.face_enroll_btn = QPushButton("Refresh enrollment")
        self.face_enroll_btn.setObjectName("primaryButton")
        self.face_enroll_btn.setMinimumHeight(36)
        self.face_enroll_btn.clicked.connect(lambda: self._run_enroll("face"))
        enroll_layout.addWidget(self.face_enroll_btn, 1, 1, 1, 2)
        self.face_enrolled_list = QListWidget()
        self.face_enrolled_list.setMinimumHeight(90)
        self.face_enrolled_list.setMaximumHeight(200)
        self.face_enrolled_list.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        enroll_layout.addWidget(QLabel("Enrolled identities:"), 2, 0)
        enroll_layout.addWidget(self.face_enrolled_list, 3, 0, 1, 3)
        layout.addWidget(enroll_gb)

        query_gb = QGroupBox("Identify")
        query_gb.setMinimumHeight(180)
        query_layout = QGridLayout(query_gb)
        query_layout.addWidget(QLabel("Select a photo to identify, then click Identify."), 0, 0, 1, 3)
        sel_identify_face = QPushButton("Select photo to identify")
        sel_identify_face.setMinimumHeight(40)
        sel_identify_face.clicked.connect(lambda: self._select_photo_to_identify("face"))
        query_layout.addWidget(sel_identify_face, 1, 0, 1, 2)
        self.face_query_path = QLineEdit()
        self.face_query_path.setPlaceholderText("No photo selected — click the button above")
        self.face_query_path.setReadOnly(True)
        self.face_query_path.setMinimumWidth(240)
        self.face_query_path.setMinimumHeight(36)
        self.face_query_path.textChanged.connect(lambda t: self.face_query_path.setToolTip(t or "No photo selected"))
        query_layout.addWidget(self.face_query_path, 2, 0)
        query_layout.setColumnStretch(0, 1)
        self.face_browse_query = QPushButton("Browse...")
        self.face_browse_query.setMinimumHeight(36)
        self.face_browse_query.clicked.connect(lambda: self._browse_query("face"))
        query_layout.addWidget(self.face_browse_query, 2, 1)
        self.face_identify_btn = QPushButton("Identify")
        self.face_identify_btn.setObjectName("primaryButton")
        self.face_identify_btn.setMinimumHeight(40)
        self.face_identify_btn.clicked.connect(lambda: self._run_identify("face"))
        query_layout.addWidget(self.face_identify_btn, 3, 0, 1, 2)
        layout.addWidget(query_gb)

        preview_gb_face = QGroupBox("Preview")
        preview_layout_face = QVBoxLayout(preview_gb_face)
        self.face_preview = QLabel()
        self.face_preview.setAlignment(Qt.AlignCenter)
        self.face_preview.setMinimumHeight(140)
        self.face_preview.setMaximumHeight(200)
        self.face_preview.setObjectName("previewLabel")
        self.face_preview.setText("No image selected")
        preview_layout_face.addWidget(self.face_preview)
        layout.addWidget(preview_gb_face)

        layout.addWidget(QLabel("Results:"))
        self.face_results = QTableWidget()
        self.face_results.setColumnCount(2)
        self.face_results.setHorizontalHeaderLabels(["Image", "Identity"])
        self.face_results.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.face_results.setMinimumHeight(180)
        self.face_results.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.face_results.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.face_results.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(self.face_results, 1)

        scroll = QScrollArea()
        scroll.setWidget(content)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setObjectName("tabScrollArea")
        tab_layout = QVBoxLayout(self.tab_face)
        tab_layout.setContentsMargins(0, 0, 0, 0)
        tab_layout.addWidget(scroll)

    def _add_menu_and_status(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")
        gen_action = QAction("Generate sample fingerprints...", self)
        gen_action.triggered.connect(self._generate_samples)
        file_menu.addAction(gen_action)
        file_menu.addSeparator()
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        help_menu = menubar.addMenu("Help")
        about_action = QAction("About", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)

        self.statusBar().showMessage("Ready — no webcam or hardware required.")

    def _log(self, msg: str):
        self.log.append(msg)
        self.log.verticalScrollBar().setValue(self.log.verticalScrollBar().maximum())

    def _auto_load_enrollment(self):
        """Load saved enrollment from disk on startup (so closing the app doesn't lose data)."""
        self._enroll_worker = EnrollWorker("fingerprint", config.FINGERPRINT_ENROLL_DIR, self)
        self._enroll_worker.progress.connect(self._log)
        self._enroll_worker.finished_success.connect(self._on_auto_fingerprint_done)
        self._enroll_worker.finished_error.connect(self._on_auto_fingerprint_error)
        self._enroll_worker.start()

    def _on_auto_fingerprint_done(self, data):
        self.fingerprint_db = data
        self.fp_enrolled_list.clear()
        for identity in sorted(data.keys()):
            count = len(data[identity])
            self.fp_enrolled_list.addItem(f"{identity} ({count} sample(s))")
        self._log("Fingerprint enrollment loaded from disk.")
        self._run_auto_face_enrollment()

    def _on_auto_fingerprint_error(self, err: str):
        self._log("No fingerprint data on disk (or error).")
        self._run_auto_face_enrollment()

    def _run_auto_face_enrollment(self):
        self._enroll_worker = EnrollWorker("face", config.FACE_ENROLL_DIR, self)
        self._enroll_worker.progress.connect(self._log)
        self._enroll_worker.finished_success.connect(self._on_auto_face_done)
        self._enroll_worker.finished_error.connect(self._on_auto_face_error)
        self._enroll_worker.start()

    def _on_auto_face_done(self, data):
        self.face_ids, self.face_features = data
        self.face_enrolled_list.clear()
        from collections import Counter
        for uid, c in sorted(Counter(self.face_ids).items()):
            self.face_enrolled_list.addItem(f"{uid} ({c} face(s))")
        self._log("Face enrollment loaded from disk. Ready.")

    def _on_auto_face_error(self, err: str):
        self._log("No face data on disk (or error). Ready.")

    def _browse_enroll(self, mode: str):
        path = QFileDialog.getExistingDirectory(self, "Select enrollment folder")
        if path:
            if mode == "fingerprint":
                self.fp_enroll_path.setText(path)
            else:
                self.face_enroll_path.setText(path)
            self._update_preview(mode, path, is_folder=True)

    def _select_photo_to_identify(self, mode: str):
        """Simple: pick one image file for identification."""
        path, _ = QFileDialog.getOpenFileName(
            self, "Select photo to identify",
            "", "Images (*.png *.jpg *.jpeg *.bmp *.tif *.tiff);;All (*)"
        )
        if path:
            if mode == "fingerprint":
                self.fp_query_path.setText(path)
            else:
                self.face_query_path.setText(path)
            self._update_preview(mode, path, is_folder=False)

    def _add_person_from_photo(self, mode: str):
        """Easy flow: choose photo → enter name → app creates folder and enrolls."""
        path, _ = QFileDialog.getOpenFileName(
            self, "Choose photo for this person",
            "", "Images (*.png *.jpg *.jpeg *.bmp *.tif *.tiff);;All (*)"
        )
        if not path:
            return
        name, ok = QInputDialog.getText(self, "Name", "Enter name for this person:")
        if not ok or not name or not name.strip():
            return
        # Sanitize name for folder (letters, numbers, spaces → underscore)
        folder_name = re.sub(r"[^\w\s\-]", "", name.strip())
        folder_name = folder_name.replace(" ", "_") or "person"
        folder_name = folder_name[:60]
        enroll_dir = config.FINGERPRINT_ENROLL_DIR if mode == "fingerprint" else config.FACE_ENROLL_DIR
        person_dir = os.path.join(enroll_dir, folder_name)
        try:
            os.makedirs(person_dir, exist_ok=True)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Cannot create folder: {e}")
            return
        ext = os.path.splitext(path)[1].lower() or ".png"
        if ext not in config.IMAGE_EXTENSIONS:
            ext = ".png"
        existing = os.listdir(person_dir)
        n = 1
        while f"image_{n}{ext}" in existing:
            n += 1
        dest = os.path.join(person_dir, f"image_{n}{ext}")
        try:
            shutil.copy2(path, dest)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Cannot copy image: {e}")
            return
        self._log(f"[{mode}] Added '{name}' from photo. Enrolling...")
        self._set_busy(True)
        self._enroll_worker = EnrollWorker(mode, enroll_dir, self)
        self._enroll_worker.progress.connect(self._log)
        self._enroll_worker.finished_success.connect(lambda data: self._on_enroll_done(mode, data))
        self._enroll_worker.finished_error.connect(self._on_enroll_error)
        self._enroll_worker.start()

    def _browse_query(self, mode: str):
        # Allow folder or file
        path, _ = QFileDialog.getOpenFileName(
            self, "Select query image or cancel to choose folder",
            "", "Images (*.png *.jpg *.jpeg *.bmp *.tif *.tiff);;All (*)"
        )
        if path:
            if mode == "fingerprint":
                self.fp_query_path.setText(path)
            else:
                self.face_query_path.setText(path)
            self._update_preview(mode, path, is_folder=False)
        else:
            path = QFileDialog.getExistingDirectory(self, "Select query folder")
            if path:
                if mode == "fingerprint":
                    self.fp_query_path.setText(path)
                else:
                    self.face_query_path.setText(path)
                self._update_preview(mode, path, is_folder=True)

    def _first_image_path(self, path: str, is_folder: bool) -> str:
        """Return path to first image file found under path (file or directory)."""
        if not path:
            return ""
        if not is_folder and os.path.isfile(path) and path.lower().endswith(config.IMAGE_EXTENSIONS):
            return path
        if not os.path.isdir(path):
            return ""
        for name in sorted(os.listdir(path)):
            full = os.path.join(path, name)
            if os.path.isfile(full) and name.lower().endswith(config.IMAGE_EXTENSIONS):
                return full
            if os.path.isdir(full):
                sub = self._first_image_path(full, True)
                if sub:
                    return sub
        return ""

    def _load_pixmap(self, path: str) -> QPixmap:
        """Load image from path; support formats via OpenCV if needed."""
        pix = QPixmap(path)
        if not pix.isNull():
            return pix
        try:
            import cv2
            img = cv2.imread(path)
            if img is None:
                return QPixmap()
            h, w, ch = img.shape
            bytes_per_line = ch * w
            fmt = QImage.Format_RGB888
            rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            qimg = QImage(rgb.data, w, h, bytes_per_line, fmt)
            return QPixmap.fromImage(qimg)
        except Exception:
            return QPixmap()

    def _update_preview(self, mode: str, path: str, is_folder: bool):
        """Show selected image in the tab's preview area (modern card style)."""
        label = self.fp_preview if mode == "fingerprint" else self.face_preview
        img_path = self._first_image_path(path, is_folder)
        if not img_path:
            label.setText("No image selected")
            label.setPixmap(QPixmap())
            return
        pix = self._load_pixmap(img_path)
        if pix.isNull():
            label.setText("Could not load image")
            label.setPixmap(QPixmap())
            return
        max_w, max_h = 320, 200
        scaled = pix.scaled(max_w, max_h, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        label.setPixmap(scaled)
        label.setText("")

    def _run_enroll(self, mode: str):
        if mode == "fingerprint":
            enroll_dir = self.fp_enroll_path.text().strip()
        else:
            enroll_dir = self.face_enroll_path.text().strip()
        if not enroll_dir or not os.path.isdir(enroll_dir):
            QMessageBox.warning(self, "Invalid path", "Please select a valid enrollment folder.")
            return
        self._set_busy(True)
        self._log(f"[{mode}] Enrolling from: {enroll_dir}")
        self._enroll_worker = EnrollWorker(mode, enroll_dir, self)
        self._enroll_worker.progress.connect(self._log)
        self._enroll_worker.finished_success.connect(lambda data: self._on_enroll_done(mode, data))
        self._enroll_worker.finished_error.connect(self._on_enroll_error)
        self._enroll_worker.start()

    def _on_enroll_done(self, mode: str, data):
        self._set_busy(False)
        if mode == "fingerprint":
            self.fingerprint_db = data
            self.fp_enrolled_list.clear()
            for identity in sorted(data.keys()):
                count = len(data[identity])
                self.fp_enrolled_list.addItem(f"{identity} ({count} sample(s))")
        else:
            self.face_ids, self.face_features = data
            self.face_enrolled_list.clear()
            from collections import Counter
            for uid, c in sorted(Counter(self.face_ids).items()):
                self.face_enrolled_list.addItem(f"{uid} ({c} face(s))")
        self._log(f"[{mode}] Enrollment completed successfully.")

    def _on_enroll_error(self, err: str):
        self._set_busy(False)
        QMessageBox.critical(self, "Enrollment error", err)
        self._log(f"Error: {err}")

    def _run_identify(self, mode: str):
        if mode == "fingerprint":
            if self.fingerprint_db is None:
                QMessageBox.warning(self, "Not enrolled", "Enroll fingerprints first.")
                return
            query_path = self.fp_query_path.text().strip()
            enrolled_data = self.fingerprint_db
            results_table = self.fp_results
        else:
            if not self.face_ids:
                QMessageBox.warning(self, "Not enrolled", "Enroll faces first.")
                return
            query_path = self.face_query_path.text().strip()
            enrolled_data = (self.face_ids, self.face_features)
            results_table = self.face_results

        if not query_path:
            QMessageBox.warning(self, "No photo selected", "Please click 'Select photo to identify' first and choose an image.")
            return

        # Collect paths: single file or all images in folder
        if os.path.isfile(query_path) and query_path.lower().endswith(config.IMAGE_EXTENSIONS):
            query_paths = [query_path]
        elif os.path.isdir(query_path):
            query_paths = [
                os.path.join(query_path, f)
                for f in sorted(os.listdir(query_path))
                if f.lower().endswith(config.IMAGE_EXTENSIONS)
            ]
        else:
            QMessageBox.warning(self, "Invalid path", "Query path must be an image file or a folder containing images.")
            return

        if not query_paths:
            QMessageBox.warning(self, "No images", "No image files found in the query path.")
            return

        self._set_busy(True)
        results_table.setRowCount(0)
        self._log(f"[{mode}] Identifying {len(query_paths)} image(s)...")
        self._identify_worker = IdentifyWorker(mode, query_paths, enrolled_data, self)
        self._identify_worker.progress.connect(self._log)
        self._identify_worker.result_item.connect(
            lambda name, identity: self._add_result_row(results_table, name, identity)
        )
        self._identify_worker.finished_success.connect(self._on_identify_done)
        self._identify_worker.finished_error.connect(self._on_identify_error)
        self._identify_worker.start()

    def _add_result_row(self, table: QTableWidget, name: str, identity: str):
        row = table.rowCount()
        table.insertRow(row)
        table.setItem(row, 0, QTableWidgetItem(name))
        table.setItem(row, 1, QTableWidgetItem(identity))

    def _on_identify_done(self, results):
        self._set_busy(False)
        self._log("Identification completed.")

    def _on_identify_error(self, err: str):
        self._set_busy(False)
        QMessageBox.critical(self, "Identification error", err)
        self._log(f"Error: {err}")

    def _set_busy(self, busy: bool):
        self.progress_bar.setVisible(busy)
        if busy:
            self.progress_bar.setRange(0, 0)  # indeterminate
        for btn in [
            self.fp_enroll_btn, self.fp_identify_btn, self.fp_add_person_btn,
            self.face_enroll_btn, self.face_identify_btn, self.face_add_person_btn,
        ]:
            btn.setEnabled(not busy)

    def _generate_samples(self):
        self._log("Generating sample fingerprint images...")
        self._samples_worker = GenerateSamplesWorker(self)
        self._samples_worker.progress.connect(self._log)
        self._samples_worker.finished_success.connect(self._on_samples_done)
        self._samples_worker.finished_error.connect(self._on_samples_error)
        self._samples_worker.start()

    def _on_samples_done(self):
        self._log("Sample fingerprints created. Use Enrollment folder: data/fingerprints/enrolled")
        QMessageBox.information(
            self,
            "Samples generated",
            "Sample fingerprint images have been created in:\n"
            "  data/fingerprints/enrolled/\n"
            "  data/fingerprints/query/\n\n"
            "Switch to Fingerprint tab and click Enroll, then Identify."
        )

    def _on_samples_error(self, err: str):
        QMessageBox.critical(self, "Error", err)
        self._log(f"Error: {err}")

    def _show_about(self):
        QMessageBox.about(
            self,
            "About Biometric Systems",
            "Biometric recognition module (Fingerprint & Face)\n"
            "using image files only — no webcam or fingerprint hardware.\n\n"
            "Python + OpenCV + PyQt5\n"
            "Sapienza University — Master course project."
        )
