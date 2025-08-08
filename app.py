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
spt_dir = None  # let user set this
mod_folders = []  # pass mod object with data
mod_configs = []
bepinex_mods = []  # build then append? maybe just append to mod_configs


class Api:
    def select_SPT_mods_directory(self):
        return select_SPT_mods_directory()

    def scrape_configs_from_mod_direcory(self):
        return scrape_configs_from_mod_direcory()

    def write_config(self, config_path, data):
        return write_config(config_path, data)

    def set_spt_install_dir(self, path):
        return set_spt_install_dir()

    def scrape_bepinex(self):
        return scrape_bepinex()

    def get_spt_install_dir(self):
        return spt_dir

    def get_mod_folders(self):
        return mod_folders

    def get_mod_configs(self):
        return mod_configs


@app.route("/")
def index():
    return render_template("index.html")


def run_flask():
    app.run(host="127.0.0.1", port=5000, debug=False)


def scrape_bepinex():
    # scrape and append bepinex configs
    # use spt_dir to get relative bepinex to root server mods folder.
    # it would be user/mods/ up two folders then through root -> bepinex -> config -> all files there
    global spt_dir
    global mod_configs
    mod_configs.clear()  # clear mod config on load (add a toggle between the two mod types)
    bepinex_config_folder = os.path.join(
        spt_dir, "..", "..", "BepInEx", "config"
    )  # loop and get all files from this folder

    if not os.path.isdir(bepinex_config_folder):
        print(f"bepinex config folder not found: {bepinex_config_folder}")
        return

    for file in os.listdir(bepinex_config_folder):
        try:
            file_path = os.path.join(bepinex_config_folder, file)
            if os.path.isfile(file_path):
                with open(file_path, "r", encoding="utf-8") as file:
                    config_data = file.read()

            mod_configs.append(
                {
                    "mod_name": os.path.basename(file_path),
                    "mod_path": file_path,
                    "mod_readme": None,  # no readme for client mods
                    "config_path": file_path,
                    "config_data": config_data,
                    "mod_type": "client",
                }
            )

            print(f"Loaded config from {bepinex_config_folder}")

        except Exception as e:
            print(f"Failed to load config from {bepinex_config_folder}: {e}")
        else:
            print(f"No config.json found in {bepinex_config_folder}")


def scrape_configs_from_mod_direcory():
    mod_configs.clear()
    for folder in mod_folders:
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

                possible_readmes = [
                    "README.md",
                    "readme.md",
                    "README.txt",
                    "readme.txt",
                ]
                readme_path = None

                for readme in possible_readmes:
                    candidate = os.path.join(folder, readme)
                    if os.path.isfile(candidate):
                        readme_path = candidate
                        break

                readme_content = None
                if readme_path:
                    with open(readme_path, "r", encoding="utf-8") as file:
                        readme_content = file.read()

                mod_configs.append(
                    {
                        "mod_name": os.path.basename(folder),
                        "mod_path": folder,
                        "mod_readme": readme_content,
                        "config_path": config_path,
                        "config_data": config_data,
                        "mod_type": "server",  # set this to client when selecting client mods
                    }
                )
                print(f"Loaded config from {config_path}")

            except Exception as e:
                print(f"Failed to load config from {folder}: {e}")
        else:
            print(f"No config.json found in {folder}")


# get mod dirs from spt user/mods directory
def select_SPT_mods_directory():
    global spt_dir, mod_folders
    mod_folders.clear()
    result = window.create_file_dialog(webview.FOLDER_DIALOG)
    if result:
        spt_dir = result[0]
        print(f"Selected SPT directory: {spt_dir}")
        for folder in os.listdir(spt_dir):
            full_path = os.path.join(spt_dir, folder)
            if os.path.isdir(full_path):
                mod_folders.append(full_path)
        return {
            "status": "success",
            "spt_dir": spt_dir,
            "mod_folders": mod_folders,
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
    global spt_dir, mod_folders
    spt_dir = path
    mod_folders.clear()
    if os.path.isdir(path):
        for folder in os.listdir(path):
            full_path = os.path.join(path, folder)
            mod_folders.append(full_path)
        return {"status": "success", "spt_dir": spt_dir}
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
