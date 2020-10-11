import winreg
import os.path
import sys

DEFAULT_CONFIG = {"SteamLibraryPath" : "",
                  "PatcherPath" : "",
                  "InstallCSSTweaks" : "1",
                  "EnablePlayButtonBox" : "0",
                  "EnableVerticalNavBar" : "0",
                  "EnableClassicLayout" : "0",
                  "InstallWithDarkLibrary" : "0"}
user_config = {}

def find_library_dir():
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "SOFTWARE\Valve\Steam");
    steam_path = winreg.QueryValueEx(key, "SteamPath")[0]
    print(steam_path)
    steamui_path = steam_path.replace("/","\\") + "\steamui"
    print(steamui_path)
    return steamui_path


### Loading config
def load_config():
    config_dict = {}
    if not os.path.isfile("oldglory_config.cfg") :
        return DEFAULT_CONFIG
    else :
        with open ("oldglory_config.cfg", newline='', encoding="UTF-8") as fi:
            lines = filter(None, (line.rstrip() for line in fi))
            for line in lines:
                if not line.startswith('###'):
                    try:
                        (key, val) = line.rstrip().replace(" ", "").split("=")
                        config_dict[key] = val
                    except Exception as e:
                        print("Error with line in config: " + line + " Skipping.", file=sys.stderr)               
    return config_dict  
    
