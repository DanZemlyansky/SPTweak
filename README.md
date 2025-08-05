# 🛠️ SPTweak – Local Config Editor for SPT Mods
# requires an spt install or atleast a directory with a modfolder/config.json or modfolder/config/config.json path*

**SPTweak** is a desktop-style tool built with Python, Flask, and PyWebView that helps you easily browse, view, and edit `.json` config files from your installed SPT mods. built this to get familiar with flask and because i have a ton of mods on my server and i find myself editing config files alot 😅


---

## 💡 Features

- 📁 Pick your local SPT mods folder
- 🔍 Scans all mod folders for `.json` config files
- 📝 View and edit JSON configs in a simple interface
- 💾 Save changes directly back to the correct mod folder
- 🖥️ Packaged with a native window — no browser tabs required


## TODO : 

- add parsing for mods using jsonc
- add support for plugin/client side mods
- add a sidebar readme display associated with each mod so its easier to reference what everything does
- improve error handling
- improve general editor experience
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
- Git (optional)

### ▶️ Run Locally

```bash

python -m venv venv
venv\Scripts\activate  

pip install flask pywebview

python app.py
