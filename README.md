# SPTweak: Local Config Editor for SPT Mods

**SPTweak** is a local mod config management tool for [Single Player Tarkov](https://github.com/sp-tarkov) built with Python, Flask, and PyWebView that helps you browse, view, and edit `.json` , `jsonc` config files from your installed SPT mods. built this to get familiar with flask and because i have a ton of mods on my server and i find myself editing config files alot 😅


---

## 💡 Use

- 📁 Pick your local SPT mods folder
- 🔍 Scans all mod folders for `.json` or `jsonc` config files
- 📝 View and edit what you need
- 💾 Save changes and save opening 10 windows in explorer


## TO DO : 

- add parsing for mods using jsonc
- ~~add support for plugin/client side mods~~
- ~~add a sidebar readme display associated with each mod so its easier to reference what everything does~~
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

git clone https://github.com/DanZemlyansky/SPTweak.git
cd SPTweak

    Create and activate a virtual environment (recommended):

    On Windows:

    python -m venv venv
    venv\Scripts\activate

    On macOS/Linux:

    python3 -m venv venv
    source venv/bin/activate

    Install dependencies:

    pip install -r requirements.txt

    Run the Flask server:

    python app.py

    or build the app using pyinstaller
