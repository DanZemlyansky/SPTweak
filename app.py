from flask import Flask, render_template
import webview
import threading
import time
import os
import json
import sys


if getattr(sys, "frozen", False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.abspath(".")

template_folder = os.path.join(base_path, "templates")

app = Flask(__name__, template_folder=template_folder)

window = None
sptInstallDir = None  #let user set this
modFolders = []  #pass mod object with data
modConfigs = []
bepinex_mods


class Api:
    def select_SPT_mods_directory(self):
        return select_SPT_mods_directory()

    def scrape_configs_from_mod_direcory(self):
        return scrape_configs_from_mod_direcory()

    def write_config(self, config_path, data):
        return write_config(config_path, data)

    def set_spt_install_dir(self, path):
        return set_spt_install_dir()

    def get_spt_install_dir(self):
        return sptInstallDir

    def get_mod_folders(self):
        return modFolders

    def get_mod_configs(self):
        return modConfigs


@app.route("/")
def index():
    return render_template("index.html")


def run_flask():
    app.run(host="127.0.0.1", port=5000, debug=False)


def scrape_bepinex(): #scrape and append bepinex configs 
    #use sptinstallDir to get relative bepinex to root server mods folder.
    # it would be user/mods/ up two folders then through root -> bepinex -> config -> all files there
    
    return

def scrape_configs_from_mod_direcory():
    modConfigs.clear()
    for folder in modFolders:
        possible_paths = [
            os.path.join(folder, "config.json"),
            os.path.join(folder, "config", "config.json"),
        ]
        config_path = None
        for path in possible_paths:
            if os.path.isfile(path):
                config_path = path
                break

        if config_path:
            try:
                with open(config_path, "r", encoding="utf-8") as file:
                    config_data = json.load(file)
                    
                possible_readmes = ["README.md" , "readme.md" , "README.txt" , "readme.txt"]
                readme_path = None
                
                for readme in possible_readmes:
                    candidate = os.path.join(folder , readme)
                    if os.path.isfile(candidate):
                        readme_path = candidate
                        break
                        
                readme_content= None
                if readme_path:
                    with open(readme_path , 'r' , encoding='utf-8') as f:
                        readme_content = f.read()        
                
                modConfigs.append(
                    {
                        "mod_name": os.path.basename(folder),
                        "mod_path": folder,
                        "mod_readme":readme_content,
                        "config_path": config_path,
                        "config_data": config_data,
                        "mod_type": "server"
                    }
                )
                print(f"Loaded config from {config_path}")

            except Exception as e:
                print(f"Failed to load config from {folder}: {e}")
        else:
            print(f"No config.json found in {folder}")


# get mod dirs from spt user/mods directory
def select_SPT_mods_directory():
    modFolders.clear()
    global sptInstallDir, modFolders
    result = window.create_file_dialog(webview.FOLDER_DIALOG)
    if result:
        sptInstallDir = result[0]
        print(f"Selected SPT directory: {sptInstallDir}")
        for folder in os.listdir(sptInstallDir):
            full_path = os.path.join(sptInstallDir, folder)
            if os.path.isdir(full_path):
                modFolders.append(full_path)
        return {
            "status": "success",
            "sptInstallDir": sptInstallDir,
            "modFolders": modFolders,
        }
    else:
        print("No directory selected.")
        return {"status": "cancel"}


# def read_config(config_path):
#     try:
#         with open(config_path, 'r', encoding='utf-8') as file:
#             return json.load(file)
#     except Exception as e:
#         print(f"Error reading config file {config_path}: {e}")
#         return None


def write_config(config_path, data):
    try:
        with open(config_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
        print(f"Config written to {config_path}")
    except Exception as e:
        print(f"Error writing config file {config_path}: {e}")


def set_spt_install_dir(path):
    global sptInstallDir, modFolders
    sptInstallDir = path
    modFolders.clear()
    if os.path.isdir(path):
        for folder in os.listdir(path):
            full_path = os.path.join(path, folder)
            modFolders.append(full_path)
        return {"status": "success", "sptInstallDir": sptInstallDir}  
    else:
        return {"status": "error", "error": "Invalid path"}


if __name__ == "__main__":
    api = Api()
    threading.Thread(target=run_flask, daemon=True).start()
    time.sleep(1)
    window = webview.create_window(
        "SPTweak", "http://127.0.0.1:5000", width=900, height=670, js_api=api
    )
    webview.start()
