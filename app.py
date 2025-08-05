from flask import Flask, render_template
import webview
import threading
import time
import os
import json

app = Flask(__name__)
window = None  
sptInstallDir = None #let user set this
modFolders = [] #pass mod object with data 
modConfigs = []

class Api:
    def select_SPT_mods_directory(self):
        return select_SPT_mods_directory()
    
    def scrape_configs_from_mod_direcory(self):
        return scrape_configs_from_mod_direcory()
    
    def write_config(self, config_path, data):
        return write_config(config_path, data)    

@app.route('/')
def index():
    return render_template('index.html') 

def run_flask():
    app.run(host='127.0.0.1', port=5000, debug=False)
    
def scrape_configs_from_mod_direcory():
    global modConfigs
    modConfigs.clear()  

    for folder in modFolders:
        config_path_root = os.path.join(folder, 'config.json')
        config_path_nested = os.path.join(folder, 'config', 'config.json')

        config_path = None
        if os.path.isfile(config_path_root):
            config_path = config_path_root
        elif os.path.isfile(config_path_nested):
            config_path = config_path_nested

        if config_path:
            try:
                with open(config_path, 'r', encoding='utf-8') as file:
                    config_data = json.load(file)

                modConfigs.append({
                    'mod_path': folder,
                    'config_path': config_path,
                    'config_data': config_data
                })
            except Exception as e:
                print(f"Failed to load config from {folder}: {e}")
        else:
            print(f"No config.json found in {folder}")   
            modConfigs.clear()  


#get mod dirs from spt user/mods directory
def select_SPT_mods_directory():
    global sptInstallDir, modFolders  
    result = window.create_file_dialog(webview.FOLDER_DIALOG)
    if result:
        sptInstallDir = result[0]
        print(f"Selected SPT directory: {sptInstallDir}")
        for folder in os.listdir(sptInstallDir):
            full_path = os.path.join(sptInstallDir, folder)
            if os.path.isdir(full_path):
                modFolders.append(full_path)
        return {"status": "success", "sptInstallDir": sptInstallDir, "modFolders": modFolders}
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
        with open(config_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)
        print(f"Config written to {config_path}")
    except Exception as e:
        print(f"Error writing config file {config_path}: {e}")

if __name__ == '__main__':
    api = Api()
    threading.Thread(target=run_flask, daemon=True).start()
    time.sleep(1)  
    window = webview.create_window('SPTweak', 'http://127.0.0.1:5000', width=800, height=600 , js_api=api)
    webview.start()