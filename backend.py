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


###Structure as follows
###config       > section       > prop              > attr
###CSS_CONFIG   > "What's New"  > "--WhatsNewOrder" > "desc" 

CSS_CONFIG = {"What's New" : {
                  "--WhatsNew" : {"default" : "block", "current" : "none",
                       "options": {"block", "none"},
                       "desc" : "Set to none to hide What's New"},
                  "--WhatsNewOrder" : {"default" : "0", "current" : "1",
                       "options": {"0", "1"},
                       "desc" : "Set 0 to put to top, 1 or higher to put to bottom"}
             },
             "Left Sidebar - Games List" : {
                  "--HoverOverlayPosition" : {"default" : "0", "current" : "unset",
                       "options": {"0", "unset"},
                       "desc" : "Set 0 if default JS, unset if tweaked JS"},
                  "--GameListEntrySize" : {"default" : "16px", "current" : "16px",
                       "options": {"16px", "20px"},
                       "desc" : ""},
                  "--CategoryNameHeaderSize" : {"default" : "13px", "current" : "13px",
                       "options": {"13px", "16px"},
                       "desc" : ""},
                  "--GameListZoomSize" : {"default" : "100%", "current" : "75%",
                       "options": {"75%", "100%"},
                       "desc" : "75% highly recommended for Game List similar to old Library UI. Affects GameListEntrySize and CategoryNameHeaderSize"}, 
                  "--ShowLeftSidebar" : {"default" : "flex", "current" : "flex",
                       "options": {"flex", "none"},
                       "desc" : "Set to none to hide left sidebar"}
             },
             "Right Click Context Menu" : {
                  "--ContextMenuLineHeight" : {"default" : "inherit", "current" : "16px",
                        "options": {"inherit", "16px"},
                        "desc" : "Currently will override very long category names"},
                  "--ContextMenuFontSize" : {"default" : "14px", "current" : "13px",
                        "options": {"14px", "13px"},
                        "desc" : ""}
             },
             "Game Grid" : {
                  "--RemoveShine" : {"default" : "block", "current" : "none",
                       "options": {"block","none"},
                       "desc" : "Set to none to Remove Shine/Glare on game grid images, which can cause discomfort"},
                  "--GameImageTransition" : {"default" : ".4s, .4s, .4s, .2s", "current" : "0s",
                       "options": {"0s", "2s", ".4s, .4s, .4s, .2s"},
                       "desc" : "Grid Game Images transition time. 0s for instant, 2s for smooth."},
                  "--GameImageOpacity" : {"default" : "1", "current" : "1",
                       "options": {"1", "0.7", "0.5"},
                       "desc" : 'Suggested values for "softer" images: 0.7 or 0.5'},
                  "--UninstalledGameImageOpacity" : {"default" : "1", "current" : "0.5",
                       "options": {"1", "0.5", "0.2"},
                       "desc" : "Suggested values: 0.5, 0.2"},
                  "--GameGridImageBackground" : {"default" : "inherit", "current" : "inherit",
                       "options": {"inherit", "#365d2d"},
                       "desc" : "Default is inherit, set #365d2d for a friendly green"},
                  "--GridRowGap" : {"default" : "24px", "current" : "8px",
                       "options": {"24px", "8px"},
                       "desc" : "Corresponds with JavaScript tweak - Home Page Grid Spacing."},
                  "--GridColumnGap" : {"default" : "16px", "current" : "5px",
                       "options": {"16px", "5px"},
                       "desc" : "Corresponds with JavaScript tweak - Home Page Grid Spacing."}
             },
             "Game Page Background" : {
                  "--AppPageBlur" : {"default" : "8px", "current" : "2px",
                       "options": {"8px","2px"},
                       "desc" : "Controls the blur between the Header and AppPage content. 2px for a more clean look."},
                  "--AmbientBlur" : {"default" : "black 80%", "current" : "black",
                       "options": {"black 80%", "black", "rgba(0,0,0,0)"},
                       "desc" : "Set to rgba(0,0,0,0) to remove"}
             },
             "Other" : {
                  "--VerticalNavBarOffset" : {"default" : "0px", "current" : "0px",
                       "options": {"0px"},
                       "desc" : "Leave at 0px, this var is for steam-library compatibility"}
            }}


SETTING_MAP = {"InstallCSSTweaks" : "",
                  "EnablePlayButtonBox" : {"start" : "/* PLAY BAR LAYOUT - BETA */", "end" : "/* END PLAY BAR LAYOUT */"},
                  "EnableVerticalNavBar" : {"start" : "/* VERTICAL NAV BAR", "end" : "/* END VERTICAL NAV BAR */"},
                  "EnableClassicLayout" : {"start" : "/* CLASSIC LAYOUT - BETA */", "end" : "/* END CLASSIC LAYOUT */"},
                  "InstallWithDarkLibrary" : ""
            }
def find_library_dir():
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "SOFTWARE\Valve\Steam")
    steam_path = winreg.QueryValueEx(key, "SteamPath")[0]
    print(steam_path)
    steamui_path = steam_path.replace("/","\\") + "\steamui"
    print(steamui_path)
    return steamui_path


### Loading config
def load_config():
    config_dict = {}
    config_filename = "oldglory_config.cfg"
    if not os.path.isfile(config_filename) :
        print("Config file " + config_filename + " not found. Creating copy with default options.", file=sys.stderr)
        create_config()
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

def create_config():
    print("TODO", flush=True)


### Settings (checkboxes) functions
def validate_settings(settings):
    validated_settings = []
    if "InstallCSSTweaks" not in settings:
        print("CSS Tweaks not enabled. Nothing will be applied.")
    elif "InstallCSSTweaks" in settings: #1
        validated_settings.extend(["InstallCSSTweaks"])
        if "EnablePlayButtonBox" in settings: #2
            validated_settings.extend(["EnablePlayButtonBox"])
        if "EnableClassicLayout" in settings and "EnableVerticalNavBar" in settings: #3 and #4
            validated_settings.extend(["EnableVerticalNavBar", "EnableClassicLayout"])
        elif "EnableVerticalNavBar" in settings: #3
            validated_settings.extend(["EnableVerticalNavBar"])
        if "InstallWithDarkLibrary" in settings: #5
            print("DARK STEAM")
            validated_settings.extend(["InstallWithDarkLibrary"])
        

    print(validated_settings)
    return validated_settings

def apply_settings(settings):
    with open("libraryroot.custom.css", "r", newline='', encoding="UTF-8") as f, \
         open("libraryroot.custom.temp.css", "w", newline='', encoding="UTF-8") as f1:
        for line in f:
            modified = 0

            ###validated_settings currently needs to be in the right order (top to bottom through CSS file)


            for setting in settings:
                #print(SETTING_MAP['EnablePlayButtonBox'] or "BLANK VALUE")
                print(line)
                #if SETTING_MAP[setting].start:
                    #print(SETTING_MAP.setting.start or "BLANK VALUE")
                #if SETTING_MAP[setting]["start"] in line:
                    #print("FOUND | " + line)
                #print(line, end="")
            
            '''
            for setting in settings:
                if fix in line:
                    f1.write(find_fix(line, fix))
                    modified = 1
            if modified == 0:
                f1.write(line)
            '''
    f.close()
    f1.close()


### CSS functions
def load_css_options():
    start = ["Configurable variables", ":root {"]
    end = ["}", "======"]

    loaded_css_config = {}
    
    with open('libraryroot.custom.css') as infile:
        lines = filter(None, (line.rstrip() for line in infile))
        prevline = ""
        startreading = 0
        for line in lines:
            if start[0] in prevline and start[1] in line:
                print("YAHOO")
                startreading = 1
            elif end[0] in prevline and end[1] in line:
                print("PARTYEND")
                startreading = 0
                break
            prevline = line
            if startreading == 1:
                css_line_parser(line)
    infile.close()
    print("U SEEING")
    '''
            for src, target in swap_js.items():
                line = line.replace(src, target)
            lines.append(line)
    with open('library.js', 'w') as outfile:
        for line in lines:
            outfile.write(line)
    '''

    
    return loaded_css_config

def css_line_parser(line):
    ###print("TODO", file=sys.stdout)
    try:
        if line.lstrip()[:2] == "/*":
            print("SECTION")
        elif line.lstrip()[:1] == "}":
            pass
        else:
            name = line.split(":", 1)
            value = name[1].split(";")
            desc = value[1].lstrip()
            print(name[0] + "  |  " + value[0] + "  |  " + desc)
    except:
        print("Some error at: " + line)

