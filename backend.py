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


CSS_CONFIG = {"What's New" : {
                  {"name": "--WhatsNew", "default" : "block", "current" : "none",
                       "options": {"block", "none"},
                       "desc" : "Set to none to hide What's New"},
                  {"name": "--WhatsNewOrder", "default" : "0", "current" : "1",
                       "options": {"0", "1"},
                       "desc" : "Set 0 to put to top, 1 or higher to put to bottom"}
             },
             "Left Sidebar - Games List" : {
                  {"name": "--HoverOverlayPosition", "default" : "0", "current" : "unset",
                       "options": {"0", "unset"},
                       "desc" : "Set 0 if default JS, unset if tweaked JS"},
                  {"name": "--GameListEntrySize", "default" : "16px", "current" : "16px",
                       "options": {"16px", "20px"},
                       "desc" : ""},
                  {"name": "--CategoryNameHeaderSize", "default" : "13px", "current" : "13px",
                       "options": {"13px", "16px"},
                       "desc" : ""},
                  {"name": "--GameListZoomSize", "default" : "100%", "current" : "75%",
                       "options": {"75%", "100%"},
                       "desc" : "75% highly recommended for Game List similar to old Library UI. Affects GameListEntrySize and CategoryNameHeaderSize"}, 
                  {"name": "--ShowLeftSidebar", "default" : "flex", "current" : "flex",
                       "options": {"flex", "none"},
                       "desc" : "Set to none to hide left sidebar"}
             },
             "Right Click Context Menu" : {
                  {"name": "--ContextMenuLineHeight", "default" : "20px", "current" : "16px",
                        "options": {"20px", "16px"},
                        "desc" : "Currently will override very long category names"},
                  {"name": "--ContextMenuFontSize", "default" : "14px", "current" : "13px",
                        "options": {"14px", "13px"},
                        "desc" : ""}
             },
             "Game Grid" : {
                  {"name": "--RemoveShine", "default" : "block", "current" : "none",
                       "options": {"block","none"},
                       "desc" : "Set to none to Remove Shine/Glare on game grid images, which can cause discomfort"},
                  {"name": "--GameImageTransition", "default" : ".4s, .4s, .4s, .2s", "current" : "0s",
                       "options": {"0s", "2s", ".4s, .4s, .4s, .2s"},
                       "desc" : "Grid Game Images transition time. 0s for instant, 2s for smooth."},
                  {"name": "--GameImageOpacity", "default" : "1", "current" : "1",
                       "options": {"Suggested values for "softer" images: 0.7 or 0.5"},
                       "desc" : 'Suggested values for "softer" images: 0.7 or 0.5'},
                  {"name": "--UninstalledGameImageOpacity", "default" : "1", "current" : "0.5",
                       "options": {"1", "0.5", "0.2"},
                       "desc" : "Suggested values: 0.5, 0.2"},
                  {"name": "--GameGridImageBackground", "default" : "inherit", "current" : "inherit",
                       "options": {"inherit", "#365d2d"},
                       "desc" : "Default is inherit, set #365d2d for a friendly green"}
             },
             "Game Page Background" : {
                  {"name": "--AppPageBlur", "default" : "8px", "current" : "2px",
                       "options": {"8px","2px"},
                       "desc" : "Controls the blur between the Header and AppPage content. 2px for a more clean look."},
                  {"name": "", "default" : "black 80%", "current" : "black",
                       "options": {"black 80%", "black", "rgba(0,0,0,0)"},
                       "desc" : "Set to rgba(0,0,0,0) to remove"}
             },
             "Other" : {
                  {"name": "--VerticalNavBarOffset", "default" : "0px", "current" : "0px",
                       "options": {"0px"},
                       "desc" : "Leave at 0px, this var is for steam-library compatibility"}
            }}

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
    
def load_css_options():
    return list
