# 🛠️ SPTweak – Local Config Editor for SPT Mods

**SPTweak** is a desktop-style tool built with Python, Flask, and PyWebView that helps you easily browse, view, and edit `.json` config files from your installed SPT mods.

---

## 💡 Features

- 📁 Pick your local SPT install folder
- 🔍 Scans all `user/mods/**` folders for `.json` config files
- 📝 View and edit JSON configs in a simple interface
- 💾 Save changes directly back to the correct mod folder
- 🖥️ Packaged with a native window — no browser tabs required

---

## 🧰 Technologies Used

| Stack        | Tools               |
|--------------|---------------------|
| **Backend**  | Python, Flask       |
| **Frontend** | HTML, Vanilla JS    |
| **Desktop UI** | PyWebView        |

---

## 📦 Setup Instructions

### 🔧 Requirements

- Python 3.9+
- Node.js (optional — only if using Tailwind)
- Git (optional)

### ▶️ Run Locally

```bash

python -m venv venv
venv\Scripts\activate  

pip install flask pywebview

python app.py
