import platform
import os.path
import sys
import shutil
import traceback

OS_TYPE = platform.system()
if OS_TYPE == "Windows":
    import winreg

DEFAULT_CONFIG = {"SteamLibraryPath" : "",
                  "PatcherPath" : "",
                  "" : "",
                  "InstallCSSTweaks" : "1",
                  "EnablePlayButtonBox" : "0",
                  "EnableVerticalNavBar" : "0",
                  "EnableClassicLayout" : "0",
                  "InstallWithDarkLibrary" : "0"}
user_config = {}


###Structure as follows
###config       > section       > prop              > attr
###CSS_CONFIG   > "What's New"  > "--WhatsNewOrder" > "desc" 

CSS_CONFIG = {
    "What's New" : {
        "--WhatsNew" : {
            "default" : "block",
            "current" : "block",
            "options": {"block", "none"},
            "desc" : "Set to none to hide What's New"},
        "--WhatsNewOrder" : {
            "default" : "0",
            "current" : "1",
            "options": {"0", "1"},
            "desc" : "Set 0 to put to top, 1 or higher to put to bottom"}
        },
    "Left Sidebar - Games List" : {
        "--HoverOverlayPosition" : {
            "default" : "0",
            "current" : "unset",
            "options": {"0", "unset"},
            "desc" : "Set 0 if default JS, unset if tweaked JS"},
        "--GameListEntrySize" : {
            "default" : "16px",
            "current" : "16px",
            "options": {"16px", "20px"},
            "desc" : ""},
        "--CategoryNameHeaderSize" : {
            "default" : "13px",
            "current" : "13px",
            "options": {"13px", "16px"},
            "desc" : ""},
        "--GameListZoomSize" : {
            "default" : "100%",
            "current" : "75%",
            "options": {"75%", "100%"},
            "desc" : "75% highly recommended for Game List similar to old Library UI. Affects GameListEntrySize and CategoryNameHeaderSize"},
        "--ShowLeftSidebar" : {
            "default" : "flex",
            "current" : "flex",
            "options": {"flex", "none"},
            "desc" : "Set to none to hide left sidebar"}
        },
    "Right Click Context Menu" : {
        "--ContextMenuLineHeight" : {
            "default" : "inherit",
            "current" : "16px",
            "options": {"inherit", "16px"},
            "desc" : "Currently will override very long category names"},
        "--ContextMenuFontSize" : {
            "default" : "14px",
            "current" : "13px",
            "options": {"14px", "13px"},
            "desc" : ""}
             },
    "Game Grid" : {
        "--RemoveShine" : {
            "default" : "block",
            "current" : "none",
            "options": {"block","none"},
            "desc" : "Set to none to Remove Shine/Glare on game grid images, which can cause discomfort"},
        "--GameImageTransition" : {
            "default" : ".4s, .4s, .4s, .2s",
            "current" : "0s",
            "options": {"0s", "2s", ".4s, .4s, .4s, .2s"},
            "desc" : "Grid Game Images transition time. 0s for instant, 2s for smooth."},
        "--GameImageOpacity" : {
            "default" : "1",
            "current" : "1",
            "options": {"1", "0.7", "0.5"},
            "desc" : 'Suggested values for "softer" images: 0.7 or 0.5'},
        "--UninstalledGameImageOpacity" : {
            "default" : "1",
            "current" : "0.5",
            "options": {"1", "0.5", "0.2"},
            "desc" : "Suggested values: 0.5, 0.2"},
        "--GameGridImageBackground" : {
            "default" : "inherit",
            "current" : "inherit",
            "options": {"inherit", "#365d2d"},
            "desc" : "Default is inherit, set #365d2d for a friendly green"},
        "--GridRowGap" : {
            "default" : "24px",
            "current" : "8px",
            "options": {"24px", "8px"},
            "desc" : "Corresponds with JavaScript tweak - Home Page Grid Spacing."},
        "--GridColumnGap" : {
            "default" : "16px",
            "current" : "5px",
            "options": {"16px", "5px"},
            "desc" : "Corresponds with JavaScript tweak - Home Page Grid Spacing."}
        },
    "Game Page Background" : {
        "--AppPageBlur" : {
            "default" : "8px",
            "current" : "2px",
            "options": {"8px", "2px"},
            "desc" : "Controls the blur between the Header and AppPage content. 2px for a more clean look."},
        "--AmbientBlur" : {
            "default" : "black 80%",
            "current" : "black",
            "options": {"black 80%", "black", "rgba(0,0,0,0)"},
            "desc" : "Set to rgba(0,0,0,0) to remove"}
             },
    "Other" : {
        "--VerticalNavBarOffset" : {
            "default" : "0px",
            "current" : "0px",
            "options": {"0px"},
            "desc" : "Leave at 0px, this var is for steam-library compatibility"}
        }
    }

SETTING_MAP = {"InstallCSSTweaks" : "",
                  "EnablePlayButtonBox" : {"start" : "/* PLAY BAR LAYOUT - BETA */", "end" : "/* END PLAY BAR LAYOUT */"},
                  "EnableVerticalNavBar" : {"start" : "/* VERTICAL NAV BAR - BETA - REQUIRES JS TWEAKS */", "end" : "/* END VERTICAL NAV BAR */"},
                  "EnableClassicLayout" : {"start" : "/* CLASSIC LAYOUT - BETA */", "end" : "/* END CLASSIC LAYOUT */"},
                  "InstallWithDarkLibrary" : ""
            }

ROOT_MAP = {"start" : ["Configurable variables", ":root {"],
            "end" : ["}", "======"]
            }

def OS_line_ending():
    if OS_TYPE == "Windows":
        return "\r\n"
    elif OS_TYPE ==  "Darwin":
        return "\n"
    elif OS_TYPE ==  "Linux":
        return "\n"
    
def find_library_dir():
    steamui_path = ""
    if OS_TYPE == "Windows":
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "SOFTWARE\Valve\Steam")
        steam_path = winreg.QueryValueEx(key, "SteamPath")[0]
        steamui_path = steam_path.replace("/","\\") + "\steamui"
        print(steamui_path)
    elif OS_TYPE ==  "Darwin":
        steamui_path = os.path.expandvars('$HOME') + "/Library/Application Support/Steam" + "\steamui"
    elif OS_TYPE ==  "Linux":
        steamui_path = os.path.expandvars('$HOME') + "/.steam/steam" + "\steamui"
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
        with open("oldglory_config.cfg", newline='', encoding="UTF-8") as fi:
            lines = filter(None, (line.rstrip() for line in fi))
            for line in lines:
                if not line.startswith('###'):
                    try:
                        (key, val) = line.rstrip().replace(" ", "").split("=")
                        config_dict[key] = val
                    except Exception as e:
                        print("Error with line in config: " + line + " Skipping.", file=sys.stderr)
        fi.close()
    return config_dict  

def create_config():
    with open("oldglory_config.cfg", "w", newline='', encoding="UTF-8") as config_file:
        for config in DEFAULT_CONFIG:
            line_to_write = config + "=" + DEFAULT_CONFIG[config] + "\n"
            if line_to_write == "=\n":
                line_to_write = "\n"
            config_file.write(line_to_write)
    config_file.close()


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
        

    #print(validated_settings)
    return validated_settings

def apply_css_settings(settings, settings_values):
    try:
        with open("libraryroot.custom.css", "r", newline='', encoding="UTF-8") as f, \
             open("libraryroot.custom.temp.css", "w", newline='', encoding="UTF-8") as f1:
            #lines = filter(None, (line.rstrip() for line in f))
            prevline = ""
            startreading = 0
            for line in f:
                modify = 0
                ###
                
                if ROOT_MAP["start"][0] in prevline and ROOT_MAP["start"][1] in line:
                    print("YAHOO " + line)
                    startreading = 1
                    for line in css_root_writer(CSS_CONFIG):
                        f1.write(line + OS_line_ending())
                    
                elif ROOT_MAP["end"][0] in prevline and ROOT_MAP["end"][1] in line:
                    print("PARTYEND")
                    startreading = 0
                prevline = line

                if startreading == 0:
                    for setting in settings_values:
                        ###
                        if 'start' in SETTING_MAP[setting]:
                            start_string = SETTING_MAP[setting]['start']
                            end_string = SETTING_MAP[setting]['end']
                            if start_string in line:
                                if start_string + "/*" in line:
                                    print(setting + " CSS Start commented out")
                                    print("Current Line | " + line)
                                    if settings_values[setting] == 1 and setting in settings:
                                        modify = 1
                                        f1.write(start_string + OS_line_ending())
                                else:
                                    if settings_values[setting] == 0:
                                        modify = 1
                                        f1.write(start_string + "/*" + OS_line_ending())
                                        print(setting + " CSS Start not commented out (enabled)")
                            if end_string in line:
                                if "*/" + end_string in line:
                                    print(setting + " CSS End commented out")
                                    print("Current Line | " + line)
                                    if settings_values[setting] == 1 and setting in settings:
                                        modify = 1
                                        f1.write(end_string + OS_line_ending())
                                else:
                                    if settings_values[setting] == 0:
                                        modify = 1
                                        f1.write("*/" + end_string + OS_line_ending())
                                        print(setting + " CSS End not commented out (enabled)")
                elif startreading == 1:
                    modify = 1
                if modify == 0:
                    f1.write(line)
        f.close()
        f1.close()

        ###
        shutil.move("libraryroot.custom.css", "libraryroot.custom.css.backup")
        shutil.move("libraryroot.custom.temp.css", "libraryroot.custom.css")
        
    except FileNotFoundError:
        print("libraryroot.custom.css not found", file=sys.stderr)

'''
def strip_tag(s, subs):
    i = s.index(subs)
    return s[:i+len(subs)]
'''

### CSS functions

### Triggers on Reload Config (button)
### Create CSS Config dict from :root in css file
def load_css_options():

    loaded_css_config = {}
    try:
        with open('libraryroot.custom.css', newline='', encoding="UTF-8") as infile:
            lines = filter(None, (line.rstrip() for line in infile))
            prevline = ""
            startreading = 0
            sectionkey = ""
            for line in lines:
                if ROOT_MAP["start"][0] in prevline and ROOT_MAP["start"][1] in line:
                    #print("YAHOO")
                    #print(line)
                    startreading = 1
                elif ROOT_MAP["end"][0] in prevline and ROOT_MAP["end"][1] in line:
                    #print("PARTYEND")
                    #print(line)
                    startreading = 0
                    break
                prevline = line
                if startreading == 1:
                    css_line_values = css_line_parser(line)
                    if css_line_values == "brace":
                        pass
                    elif "section" in css_line_values:
                        sectionkey = css_line_values["section"]
                        loaded_css_config[sectionkey] = {}
                    elif all (k in css_line_values for k in ("name", "default", "current", "desc")):
                        propkey = css_line_values["name"]
                        loaded_css_config[sectionkey][propkey] = {}
                        loaded_css_config[sectionkey][propkey]["default"] = css_line_values["default"]
                        loaded_css_config[sectionkey][propkey]["current"] = css_line_values["current"]
                        ### create options attr
                        #print(CSS_CONFIG.get(sectionkey, {}).get(propkey))
                        if exists_key_value := CSS_CONFIG.get(sectionkey, {}).get(propkey):
                            loaded_css_config[sectionkey][propkey]["options"] = CSS_CONFIG[sectionkey][propkey]["options"]
                        else:
                            print("Options not found in default, creating from default + current values")
                            loaded_css_config[sectionkey][propkey]["options"] = {css_line_values["default"], css_line_values["current"]}
                        loaded_css_config[sectionkey][propkey]["desc"] = css_line_values["desc"]
        infile.close()
        print("Loaded CSS Options.")
    except:
        print("Error loading CSS config from line: " + line, file=sys.stderr)
        print("~~~~~~~~~~")
        print(traceback.print_exc(), file=sys.stderr)
        print("~~~~~~~~~~")
        print("Using default CSS config.")
        loaded_css_config = CSS_CONFIG
    return loaded_css_config

###Parses one line of CSS file into dictionary values
def css_line_parser(line):
    try:
        if line.lstrip()[:2] == "/*":
            section = line.lstrip()[3:-3]
            return {"section" : section}
        elif line.lstrip()[:5] == ":root":
            return "brace"
        elif line.lstrip()[:1] == "}":
            return "brace"     
        else:
            name = line.lstrip().split(":", 1)
            value = name[1].lstrip().split(";")
            desc = value[1].lstrip()
            #print(name[0] + "  |  " + value[0] + "  |  " + desc)
            default = ""
            if "/* Default: " in desc:
                default = "WHAT"
                default = desc.split("/* Default: ")[1].split(".")[0]                                                            
            else:
                default = value[0]
            return {"name" : name[0], "default" : default, "current" : value[0], "desc" : desc}   
    except Exception as e:
        print("Some error in line: " + line, file=sys.stderr)
        print("~~~~~~~~~~")
        print(traceback.print_exc(), file=sys.stderr)
        print("~~~~~~~~~~")
        

#root writer
#from CSS_CONFIG dictionary to an array of lines of CSS to be written
def css_root_writer(css_config):
    print("START ROOT WRITER")
    indent = "  "
    css_lines = []
    css_lines.append(":root {")
    for key in css_config:
        print(key)
        css_lines.append(indent + "/* " + key + " */")
        #
        for prop in css_config[key]:
            css_lines.append(indent + prop + ": "
                             + css_config[key][prop]["current"] + ";  "
                             + "/* Default: " + css_config[key][prop]["default"] + ". "
                             + css_config[key][prop]["desc"] + " */")
        css_lines.append("")
    del css_lines[-1]
    css_lines.append("}")
    #print(css_lines)
    return css_lines

def css_root_writer_example():
    indent = "  "
    file = open("rootfile.css", "w", newline='', encoding="UTF-8")
    for line in css_root_writer(CSS_CONFIG):
        file.write(line + OS_line_ending())
    file.close()
    
