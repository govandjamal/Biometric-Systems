# How the GUI Works — Simple Guide

## What you see when you open the app

When you run **`python run_gui.py`**, a window opens with **two tabs**:

1. **Fingerprint** — for fingerprint images  
2. **Face** — for face photos  

You **do not need to create any folders**. The app does everything for you.

---

## Easy way: Add a person (no folders)

1. Click **"Add person — choose photo and enter name"**.
2. **Choose a photo** (one image of that person’s fingerprint or face).
3. When asked, **enter the person’s name** (e.g. *Ahmed* or *Maria*).
4. The app **creates the folder**, **saves the photo**, and **enrolls** that person automatically.
5. The name appears under **Enrolled people**.

You can add more people the same way. Each time: choose photo → enter name → done.

---

## Easy way: Identify who is in a photo

1. Click **"Select photo to identify"**.
2. **Choose one image** (the fingerprint or face you want to recognize).
3. The selected photo appears in **Preview**.
4. Click **"Identify"**.
5. The **Results** table shows: that image → **name** (if it matches someone you added) or **Unknown**.

---

## Summary (no folders needed)

| What you do | What happens |
|-------------|--------------|
| **Add person** → choose photo → enter name | App creates everything and enrolls that person. |
| **Select photo to identify** → choose image | That image is set for identification. |
| Click **Identify** | App says who it is (name or Unknown). Results appear in the table. |

**Order:** First **add** one or more people (photo + name), then **select a photo** and click **Identify** to see who it is.

---

## Other things in the window

- **Enrolled people** — List of everyone you added. You can still use **Browse** and **Refresh enrollment** if you have your own folders.
- **Preview** — Shows the photo you selected for identification.
- **Results** — Table: image name → identity (person or Unknown).
- **Log** — Messages about what the app is doing.
- **Footer** — Your name (Kofand Saedd metrocola 2239066).
- **File → Generate sample fingerprints** — Creates example fingerprint images so you can try the app without your own data.
