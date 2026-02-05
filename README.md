# Biometric Recognition Module (Image-Based)

A complete **biometric recognition system** implemented in **Python** using **OpenCV** and **NumPy**.  
Designed for use **without webcam or fingerprint hardware**: all inputs are **image files** loaded from disk.

Suitable for academic use (e.g. Master-level Biometric Systems course).

---

## Features

- **Fingerprint recognition**  
  - Load fingerprint images from folders (e.g. FVC datasets or your own images).  
  - Pipeline: preprocessing → enhancement → binarization → thinning → minutiae extraction → matching.  
  - No fingerprint sensor required.

- **Face recognition (optional)**  
  - Load face images from disk (one folder per person).  
  - Detection, alignment, feature extraction, and matching using image files only.  
  - No webcam required.

---

## Requirements

- Python 3.8+
- OpenCV, NumPy, SciPy, PyQt5 (see `requirements.txt`)

---

## Installation

```bash
cd "Biometric Systems"
pip install -r requirements.txt
```

---

## Data (no webcam / no hardware)

### Fingerprint

Place fingerprint images in:

- `data/fingerprints/enrolled/` — one image per person (or multiple per person).  
  Use subfolders named by identity, e.g. `data/fingerprints/enrolled/person_01/image.png`.

- `data/fingerprints/query/` — images to identify or verify.

You can use public datasets (e.g. **FVC2002**, **FVC2004**) by copying images into these folders.  
No camera or fingerprint reader is used.

### Face (optional)

- `data/faces/enrolled/` — one subfolder per person, each containing face images.  
- `data/faces/query/` — face images to identify.

Again, only image files; no webcam.

---

## Usage

### GUI (PyQt5) — recommended

Manage everything from a single window: enrollment, identification, and sample generation.

```bash
python run_gui.py
```

- **Fingerprint** tab: set enrollment folder (e.g. `data/fingerprints/enrolled`), click **Enroll**; set query folder or file, click **Identify**. Results appear in the table.
- **Face** tab: same workflow with `data/faces/enrolled` and `data/faces/query`.
- **File → Generate sample fingerprints**: creates synthetic data so you can test without a dataset.
- Log and status bar show progress; heavy work runs in background so the interface stays responsive.

### Command line

#### Run fingerprint pipeline (enrollment + identification)

```bash
python main.py --mode fingerprint --enroll-dir data/fingerprints/enrolled --query-dir data/fingerprints/query
```

### Run face pipeline (enrollment + identification)

```bash
python main.py --mode face --enroll-dir data/faces/enrolled --query-dir data/faces/query
```

### Generate synthetic fingerprint images for testing (no dataset needed)

```bash
python scripts/generate_sample_fingerprints.py
```

This creates sample images in `data/fingerprints/` so you can run the full pipeline without downloading FVC.

---

## Project structure

```
Biometric Systems/
├── README.md
├── requirements.txt
├── run_gui.py              # Launch PyQt5 GUI (recommended)
├── main.py                 # CLI: fingerprint or face pipeline
├── config.py               # Paths and parameters
├── gui/                    # PyQt5 interface
│   ├── __init__.py
│   ├── window.py           # Main window (tabs, enrollment, identify, log)
│   ├── workers.py           # Background threads for enroll/identify
│   └── styles.py           # Dark theme stylesheet
├── biometrics/
│   ├── __init__.py
│   ├── fingerprint/        # Fingerprint preprocessing, minutiae, matching
│   │   ├── __init__.py
│   │   ├── preprocessing.py
│   │   ├── minutiae.py
│   │   └── matching.py
│   └── face/               # Face detection, features, matching (image-based)
│       ├── __init__.py
│       ├── detection.py
│       ├── features.py
│       └── matching.py
├── data/
│   ├── fingerprints/
│   │   ├── enrolled/
│   │   └── query/
│   └── faces/
│       ├── enrolled/
│       └── query/
└── scripts/
    └── generate_sample_fingerprints.py
```

---

## References (for report)

- Maltoni et al., *Handbook of Fingerprint Recognition*, Springer.
- FVC (Fingerprint Verification Competition) datasets: http://bias.csr.unibo.it/fvc2002/ , etc.
- OpenCV documentation: https://docs.opencv.org/

---

## For your report (Sapienza / Master course)

- **Objective**: Design and implementation of a biometric module (fingerprint and face) using **image-based** input only (OpenCV + Python). No webcam or fingerprint hardware required.
- **Fingerprint**: Preprocessing (normalization, CLAHE, binarization, thinning), minutiae extraction (crossing number), and matching by minutiae comparison.
- **Face**: Detection (Haar cascade), LBP feature extraction, matching by cosine similarity.
- **Experiments**: Use FVC datasets for fingerprint (copy images into `data/fingerprints/`) or the provided synthetic samples; for face use any face image dataset (e.g. LFW, or your own folders).

## Author note

This project uses **only image files** as input. It does **not** use webcam or any fingerprint sensor, making it suitable for environments where such hardware is unavailable.
