# How to Put This Project on GitHub

Follow these steps to upload your Biometric Systems project to GitHub.

---

## 1. Create a GitHub account (if you don’t have one)

- Go to **https://github.com**
- Sign up (free)

---

## 2. Create a new repository on GitHub

1. Log in to GitHub.
2. Click the **+** (top right) → **New repository**.
3. Fill in:
   - **Repository name:** e.g. `biometric-systems` or `Biometric-Systems`
   - **Description:** e.g. `Fingerprint and face recognition (image-based, Python + OpenCV + PyQt5)`
   - **Public** (or Private if you prefer).
   - **Do not** check “Add a README” (you already have one).
4. Click **Create repository**.

---

## 3. Open terminal in your project folder

- Open **PowerShell** or **Command Prompt**.
- Go to the project folder:
  ```bash
  cd "C:\Users\Administrator\Downloads\Biometric Systems"
  ```

---

## 4. Initialize Git and add files

Run these commands **one by one**:

```bash
git init
git add .
git status
```

- `git init` — turns this folder into a Git repo.
- `git add .` — stages all files (respecting `.gitignore`).
- `git status` — shows what will be committed (you should see your code, not `__pycache__` or `data/`).

---

## 5. First commit

```bash
git commit -m "Initial commit: Biometric Systems - Fingerprint and Face (image-based)"
```

---

## 6. Connect to GitHub and push

GitHub will show you something like:

```
…or push an existing repository from the command line
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

**Replace** `YOUR_USERNAME` and `YOUR_REPO_NAME` with your real GitHub username and repo name.

Example if your username is **kofand** and repo is **biometric-systems**:

```bash
git remote add origin https://github.com/kofand/biometric-systems.git
git branch -M main
git push -u origin main
```

- When you run `git push`, GitHub may ask you to **log in** (browser or token).
- If it asks for a **password**, use a **Personal Access Token** (see below), not your GitHub password.

---

## 7. After the first push

- Refresh your repo page on GitHub — you’ll see all your files.
- The **data/** folder is **not** uploaded (it’s in `.gitignore` so your enrolled photos stay local). If you want to add sample data later, you can change `.gitignore` and commit again.

---

## If GitHub asks for a password / token

1. On GitHub: **Settings** → **Developer settings** → **Personal access tokens** → **Tokens (classic)**.
2. **Generate new token**, give it a name, check **repo**.
3. Copy the token and use it **instead of your password** when `git push` asks for a password.

---

## Quick copy-paste (after you create the repo on GitHub)

```bash
cd "C:\Users\Administrator\Downloads\Biometric Systems"
git init
git add .
git commit -m "Initial commit: Biometric Systems - Fingerprint and Face (image-based)"
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

Replace `YOUR_USERNAME` and `YOUR_REPO_NAME` with your GitHub username and repository name.
