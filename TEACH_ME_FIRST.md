# Teach Me First — Biometric Systems Project

This file explains **what to run first**, **how the project works in simple words**, **what technology is used**, and **which research papers** these ideas come from.

---

## 1. What file should I run first?

### Easiest: run the graphical interface (GUI)

1. Open a terminal in the project folder:
   ```bash
   cd "Biometric Systems"
   ```
2. Install dependencies (once):
   ```bash
   pip install -r requirements.txt
   ```
3. Start the program:
   ```bash
   python run_gui.py
   ```
4. In the window:
   - Go to **File → Generate sample fingerprints** to create test images (no dataset needed).
   - Open the **Fingerprint** tab → click **Enroll** (uses the default folder) → then **Identify**.
   - You will see results in the table and messages in the log.

**So the first file you should run is: `run_gui.py`.**

---

### Other ways to run (optional)

| What you want to do | File to run | Command |
|---------------------|-------------|--------|
| Use the GUI (recommended) | `run_gui.py` | `python run_gui.py` |
| Use the command line (fingerprint) | `main.py` | `python main.py --mode fingerprint` |
| Use the command line (face) | `main.py` | `python main.py --mode face` |
| Create sample fingerprint images only | `scripts/generate_sample_fingerprints.py` | `python scripts/generate_sample_fingerprints.py` |

---

## 2. How does it work? (Simple explanation)

The project does **two types of biometric recognition** using **only image files** (no webcam, no fingerprint sensor).

### Big picture

1. **Enrollment**: You give the system images of people (or fingers) and tell it “this is person_01”, “this is person_02”, etc. The system extracts **features** and stores them.
2. **Identification**: You give it a **new image** (a “query”). The system extracts the same kind of features and **compares** them to what was stored. It then says “this is person_01” or “Unknown”.

Everything is done **offline**: we only read image files from disk.

---

### How fingerprint recognition works here

1. **Load image** — Read a fingerprint image from a file (e.g. PNG).
2. **Preprocess** — Convert to grayscale, resize to a fixed size, **normalize** (adjust brightness/contrast), **enhance** with CLAHE (see below), then **binarize** (black and white) and **thin** the ridges (skeleton).
3. **Extract minutiae** — On the thinned image we find special points: **ridge endings** and **bifurcations** (where a ridge splits). These are the “minutiae”.
4. **Match** — For a new fingerprint we extract minutiae again. We compare positions and types of minutiae between the new image and each enrolled fingerprint. If enough of them match, we say “same person”.

So: **image → clean ridges → minutiae points → compare minutiae → identity.**

---

### How face recognition works here

1. **Load image** — Read a photo from a file.
2. **Detect face** — Find the face in the image (a rectangle around it) using a **Haar cascade** detector.
3. **Extract features** — Crop the face, resize it, and compute a **LBP (Local Binary Pattern)** histogram. This describes the texture of the face in a compact way.
4. **Match** — For a new face image we compute its LBP histogram and **compare** it (e.g. cosine similarity) to the stored ones. The best match gives the identity.

So: **image → find face → LBP features → compare features → identity.**

---

## 3. Technology used

| Technology | What it is | Where we use it |
|------------|------------|------------------|
| **Python** | Programming language | Whole project |
| **OpenCV (cv2)** | Library for image processing and computer vision | Reading images, resizing, CLAHE, binarization, face detection (Haar), basic operations |
| **NumPy** | Arrays and numerical computation | Image arrays, math for features and matching |
| **SciPy** | Scientific computing | Optional support (e.g. filters) |
| **scikit-image** | Image processing (e.g. morphology) | **Skeletonization (thinning)** of the fingerprint binary image |
| **PyQt5** | GUI framework | Buttons, tabs, tables, log, file dialogs; all the “window” you see when you run `run_gui.py` |

- **Fingerprint**: OpenCV (preprocessing, binarization), scikit-image (skeletonize), our code (minutiae extraction and matching).
- **Face**: OpenCV (Haar cascade for detection), our code (LBP histogram and matching).

No webcam or fingerprint hardware is used — only image files.

---

## 4. Research papers and references

These are **well-known books and papers** that describe the ideas and methods used in this project. You can cite them in your report.

### Fingerprint recognition (general)

- **D. Maltoni, D. Maio, A. K. Jain, S. Prabhakar**, *Handbook of Fingerprint Recognition*, 2nd ed., Springer, 2009.  
  Standard reference for fingerprint recognition: preprocessing, minutiae, matching, and evaluation.

- **A. K. Jain, L. Hong, R. Bolle**, “On-line fingerprint verification,” *IEEE Transactions on Pattern Analysis and Machine Intelligence*, vol. 19, no. 4, pp. 302–314, 1997.  
  Classic paper on fingerprint verification and minutiae.

### Preprocessing and enhancement

- **L. Hong, Y. Wan, A. K. Jain**, “Fingerprint image enhancement: algorithm and performance evaluation,” *IEEE Transactions on Pattern Analysis and Machine Intelligence*, vol. 20, no. 8, pp. 777–789, 1998.  
  Fingerprint enhancement and quality; context for methods like CLAHE and Gabor filtering.

- **K. Zuiderveld**, “Contrast Limited Adaptive Histogram Equalization,” in *Graphics Gems IV*, Academic Press, 1994.  
  **CLAHE** (Contrast Limited Adaptive Histogram Equalization) — we use this for fingerprint contrast enhancement.

### Thinning and minutiae

- **L. Lam, S. W. Lee, C. Y. Suen**, “Thinning methodologies – A comprehensive survey,” *IEEE Transactions on Pattern Analysis and Machine Intelligence*, vol. 14, no. 9, pp. 869–885, 1992.  
  Survey of thinning/skeletonization methods; our skeletonization step follows this type of approach.

- **C. L. Wilson et al.**, “Fingerprint verification based on minutiae features: a review,” *Pattern Recognition*, vol. 37, no. 3, pp. 609–625, 2004.  
  Minutiae-based fingerprint verification; ridge endings and bifurcations.

### Fingerprint databases and evaluation

- **D. Maio et al.**, “FVC2002: Second Fingerprint Verification Competition,” *Proc. ICPR*, 2002.  
  **FVC (Fingerprint Verification Competition)** — public datasets and benchmarks; you can use FVC images in this project.

### Face detection

- **P. Viola, M. Jones**, “Rapid object detection using a boosted cascade of simple features,” *Proc. IEEE CVPR*, 2001.  
  **Viola–Jones** detector; OpenCV’s **Haar cascade** face detector is based on this.

### Face recognition and LBP

- **T. Ahonen, A. Hadid, M. Pietikäinen**, “Face description with local binary patterns: Application to face recognition,” *IEEE Transactions on Pattern Analysis and Machine Intelligence*, vol. 28, no. 12, pp. 2037–2041, 2006.  
  **LBP (Local Binary Pattern)** for face description and recognition — we use LBP histograms for face features.

- **M. Pietikäinen, A. Hadid, G. Zhao, T. Ahonen**, *Computer Vision Using Local Binary Patterns*, Springer, 2011.  
  Book on LBP and its use in vision; supports the face recognition part of the project.

---

## 5. Short summary

- **Run first:** `python run_gui.py` (after `pip install -r requirements.txt`).
- **How it works:** Enrollment = store features from images; Identification = extract features from a new image and compare to stored ones. Fingerprint uses **minutiae**; face uses **LBP** and **Haar** detection.
- **Technology:** Python, OpenCV, NumPy, scikit-image, PyQt5; all from **image files**, no camera or sensor.
- **References:** The list above gives you books and papers to cite for fingerprint recognition, CLAHE, thinning, minutiae, FVC, Viola–Jones (Haar), and LBP for face recognition.

If you follow this file, you know what to run first and how to explain and reference the project simply.
