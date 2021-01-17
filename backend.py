import platform
import os
import sys
import subprocess
import shutil
import traceback
import re
from pathlib import Path
import json
import sass
from datetime import datetime, timezone
import requests

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
                  "LandscapeImages" : "0",
                  "InstallWithDarkLibrary" : "0",
                  "ThemeSelected" : "Crisp Cut"}
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
    "Game Page Layout" : {
        "--FriendsDLCScreenshotsColumnWidth" : {
            "default" : "33%",
            "current" : "57%",
            "options": {"33%", "57%"},
            "desc" : "Determines width of the Friends Who Play/Achievements/Screenshots/DLC/Trading Cards column. Friend Activity/News column will fill the rest."},
        "--SwapColumns" : {
            "default" : "right",
            "current" : "left",
            "options": {"left", "right"},
            "desc" : "Set left to swap columns."}
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
            "desc" : "Leave at 0px, this var is for steam-library compatibility and vertical nav bar"}
        }
    }

SETTING_MAP = {"SteamLibraryPath" : "",
                  "PatcherPath" : "",
                  "" : "",
                  "InstallCSSTweaks" : "",
                  "EnablePlayButtonBox" : {"filename" : "module_playbarbox"},
                  "EnableVerticalNavBar" : {"filename" : "module_verticalnavbar"},
                  "EnableClassicLayout" : {"filename" : "module_classiclayout"},
                  "LandscapeImages" : {"filename" : "module_landscapegameimages"},                
                  "InstallWithDarkLibrary" : "",
                  "ThemeSelected" : ""
                
            }

ROOT_MAP = {"start" : ["Configurable variables", ":root {"],
            "end" : ["}", "======"]
            }

PATCHED_TEXT = "/*patched*/"

#SMALL_UPDATE_FILE_LIST = get_small_update_file_list()

def get_json_data():
    json_data_filename = 'old_glory_data.json'
    try:
        with open(json_data_filename) as f:
            global json_data
            json_data = json.load(f)
        print("Loaded JSON data. " + "(" + json_data_filename + ")")
        f.close()
        return json_data
    except FileNotFoundError:
        print("JSON file " + json_data_filename + " not found.", file=sys.stderr)
    except json.decoder.JSONDecodeError as e:
        print("Error in JSON file format:", file=sys.stderr)
        print(e, file=sys.stderr)
        print_traceback()
    except:
        print("Error reading JSON file " + json_data_filename, file=sys.stderr)
        print_traceback()

def OS_line_ending():
    if OS_TYPE == "Windows":
        return "\r\n"
    elif OS_TYPE ==  "Darwin":
        return "\n"
    elif OS_TYPE ==  "Linux":
        return "\n"

# could use testing
def OS_open_file(path):
    try:
        if OS_TYPE == "Windows":
            subprocess.Popen(["explorer", path])
        elif OS_TYPE ==  "Darwin":
            subprocess.Popen(["open", "--", path])
        elif OS_TYPE ==  "Linux":
            subprocess.Popen(["xdg-open", "--", path])
        print("Opened file at: " + path)
    except:
        print_traceback()
    
def library_dir():
    steamui_path = ""
    if OS_TYPE == "Windows":
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "SOFTWARE\Valve\Steam")
        steam_path = winreg.QueryValueEx(key, "SteamPath")[0]
        steamui_path = steam_path.replace("/","\\") + "\steamui"
        #print(steamui_path)
    elif OS_TYPE ==  "Darwin":
        steamui_path = os.path.expandvars('$HOME') + "/Library/Application Support/Steam" + "/steamui"
    elif OS_TYPE ==  "Linux":
        steamui_path = os.path.expandvars('$HOME') + "/.steam/steam" + "/steamui"
    return steamui_path

def print_traceback():
    print("~~~~~~~~~~~~~~~~~~~~")
    print(traceback.format_exc(), end='', file=sys.stderr)
    print("~~~~~~~~~~~~~~~~~~~~")

### Check CSS Patched
def is_css_patched():
    patched = False
    try:
        with open(library_dir() + "/css/5.css", newline='', encoding="UTF-8") as f:
            first_line = f.readline()
        if PATCHED_TEXT in first_line:
            patched = True
        else:
            pass
            #print("css\libraryroot.css not patched.", file=sys.stderr)
        f.close()
    except:
        print("css\5.css (previously known as libraryroot.css), not found", file=sys.stderr)
        print_traceback()
    return patched

def get_current_datetime():
    date = datetime.now(timezone.utc)
    date_f = date.strftime("%Y-%m-%dT%H:%M:%SZ")
    return date_f

###
### CONFIG Functions
###

### Loading config
def load_config():
    config_dict = {}
    config_filename = "oldglory_config.cfg"
    if not os.path.isfile(config_filename) :
        print("Config file " + config_filename + " not found. Creating copy with default options.", file=sys.stderr)
        write_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG
    else :
        with open("oldglory_config.cfg", newline='', encoding="UTF-8") as fi:
            lines = filter(None, (line.rstrip() for line in fi))
            for line in lines:
                if not line.startswith('###'):
                    try:
                        #spaces?
                        #(key, val) = line.rstrip().replace(" ", "").split("=")
                        (key, val) = line.rstrip().split("=")
                        config_dict[key] = val
                    except Exception as e:
                        print("Error with line in config: " + line + " Skipping.", file=sys.stderr)
        fi.close()
    return config_dict  

def write_config(config_dict):
    with open("oldglory_config.cfg", "w", newline='', encoding="UTF-8") as config_file:
        for config in config_dict:
            line_to_write = config + "=" + str(config_dict[config]) + OS_line_ending()
            if line_to_write == "=\n":
                line_to_write = OS_line_ending()
            config_file.write(line_to_write)
    config_file.close()


### Settings (checkboxes) functions
# Need to change logic to cover "unchecking" options
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
        if "LandscapeImages" in settings: #2
            validated_settings.extend(["LandscapeImages"])
        if "InstallWithDarkLibrary" in settings: #6
            validated_settings.extend(["InstallWithDarkLibrary"])
    #print(validated_settings)
    return validated_settings

### END
###


###
### CSS functions (libraryroot.custom.css)
### if/for loops could be reduced

def write_css_settings(settings, settings_values, root_config): 
    try:
        with open("scss/libraryroot.custom.scss", "r", newline='', encoding="UTF-8") as f, \
             open("scss/libraryroot.custom.temp.scss", "w", newline='', encoding="UTF-8") as f1:

            import_prefix = '@import "./'
            start_comment = '//'
            modify = 0
            startreading = 0
            for line in f:
                if "../themes/" not in line or import_prefix in line:
                    for setting in settings_values:
                        if 'filename' in SETTING_MAP[setting]:
                            if import_prefix + SETTING_MAP[setting]['filename'] in line:
                                if line.startswith(start_comment):
                                    if settings_values[setting] == 1 and setting in settings:
                                        modify = 1
                                        f1.write(line.split(start_comment)[1].lstrip())
                                else:    
                                    if settings_values[setting] == 0:
                                        modify = 1
                                        f1.write(start_comment + " " + line)
                    if modify == 0:
                        f1.write(line)
                    modify = 0
                else:
                    f1.write(line)
        f.close()
        f1.close()
        
        ###
        shutil.move("scss/libraryroot.custom.scss", "scss/libraryroot.custom.scss.backup1")
        shutil.move("scss/libraryroot.custom.temp.scss", "scss/libraryroot.custom.scss")
            
    except:
        print("Error enabling/disabling CSS modules.", file=sys.stderr)
        print_traceback()

# Compiles libraryroot.custom.css from /scss directory
# Adds variables.css
def compile_css(json_data):
    try:
        sass.compile(dirname=('scss','.'),
                     output_style='expanded')
        with open('libraryroot.custom.css', "r", newline='', encoding="UTF-8") as f, \
             open("libraryroot.custom.temp.css", "w", newline='', encoding="UTF-8") as f1:
            for line in f:
                if json_data["CSSVariableString"] in line:
                    #print(line)
                    with open('variables.css', "r", newline='', encoding="UTF-8") as v1:
                        for variable_line in v1:
                            f1.write(variable_line)
                            #print(variable_line)
                    v1.close()
                    f1.write(OS_line_ending())
                else:
                    f1.write(line)
        f.close()
        f1.close()
    except:
        print("Error compiling SCSS to CSS", file=sys.stderr)
        print_traceback()
        
    ###
    shutil.move("libraryroot.custom.css", "libraryroot.custom.css.backup")
    shutil.move("libraryroot.custom.temp.css", "libraryroot.custom.css")


### Triggers on Reload Config (button)
### From :root in css file -> CSS Config dict
def load_css_configurables():
    css_config_filename = "variables.css"
    loaded_css_config = {}
    try:
        with open(css_config_filename, newline='', encoding="UTF-8") as infile:
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
                            print("Custom CSS variable " + css_line_values["name"] + " found, creating options as\n    Default: " +
                                  css_line_values["default"] + ", Current: " + css_line_values["current"])
                            loaded_css_config[sectionkey][propkey]["options"] = {css_line_values["default"], css_line_values["current"]}
                        loaded_css_config[sectionkey][propkey]["desc"] = css_line_values["desc"]
        infile.close()
        print("Loaded CSS Options. " + "(" + css_config_filename + ")")
    except FileNotFoundError:
        print(css_config_filename + " not found", file=sys.stderr)
    except:
        print("Error loading CSS configurables from line: " + line, file=sys.stderr)
        print_traceback()
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
            comment = value[1].lstrip()
            default = ""
            if "/* Default: " in comment:
                comment_m = comment.split("/* Default: ")[1].split(". ", 1)
                default = comment_m[0].lstrip()
                desc = comment_m[1].split("*/")[0].strip()
            else:
                default = value[0]
                desc = comment.split("/*")[1].split("*/")[0].strip()
                
            #print(name[0] + "  |  " + default + "  |  " + value[0] + "  |  " + desc)
            return {"name" : name[0], "default" : default, "current" : value[0], "desc" : desc}
    except Exception as e:
        print("Some error in line: " + line, file=sys.stderr)
        print_traceback()
        

def write_css_configurables(css_config):
    css_config_filename = "variables.css"
    to_write_lines = create_css_variables_lines(css_config)
    try:
        with open(css_config_filename, "w", newline='', encoding="UTF-8") as f:
            for line in to_write_lines[:-1]:
                f.write(line + OS_line_ending())
            f.write(to_write_lines[-1])
    except:
        print("Error writing to " + css_config_filename, file=sys.stderr)
        print_traceback()

#create css variables
#from CSS_CONFIG dictionary to an array of lines of CSS to be written
def create_css_variables_lines(css_config):
    try:
        indent = "  "
        css_lines = []
        css_lines.append("/* Configurable variables */")
        css_lines.append(":root {")
        for key in css_config:
            #print(key)
            css_lines.append(indent + "/* " + key + " */")

            for prop in css_config[key]:
                css_lines.append(indent + prop + ": "
                                 + css_config[key][prop]["current"] + ";  "
                                 + "/* Default: " + css_config[key][prop]["default"] + ". "
                                 + css_config[key][prop]["desc"] + " */")
            css_lines.append("")
        del css_lines[-1]
        css_lines.append("}")
        return css_lines
    except:
        print("Unable to generate css variables", file=sys.stderr)
        print_traceback()


### END
###



###
### APPLY CSS THEME Functions
### Simplified due to use of SCSS

### Now removes existing theme imports and adds current ones to be enabled
def enable_css_theme(theme_filename, order, json_data):
    try:
        with open("scss/libraryroot.custom.scss", "r", newline='', encoding="UTF-8") as f, \
             open("scss/libraryroot.custom.temp.scss", "w", newline='', encoding="UTF-8") as f1:
            themereading = 0
            for line in f:
                if themereading == 1:
                    if line != OS_line_ending():
                        pass
                    else:
                        if order == "before" and os.path.exists("themes/" + theme_filename):
                            #print("theme line")
                            # [1:-5] is to truncate the _ and .scss
                            f1.write('@import "../themes/' + theme_filename[1:-5] + '";' + OS_line_ending())
                        f1.write(OS_line_ending())
                        themereading = 0
                elif themereading == 2:
                    if line != OS_line_ending():
                        pass
                    else:
                        if order == "after" and os.path.exists("themes/" + theme_filename):
                            #print("theme line")
                            f1.write('@import "../themes/' + theme_filename[1:-5] + '";' + OS_line_ending())
                        f1.write(OS_line_ending())
                        themereading = 0
                        
                elif json_data["CSSBeforeThemes"] in line:
                    f1.write(line)
                    themereading = 1
                elif json_data["CSSAfterThemes"] in line:
                    f1.write(line)
                    themereading = 2
                else:
                    f1.write(line)
            if theme_filename == "_shiina.scss":
                steam_library_compat_config()
        
        f.close()
        f1.close()
        
        ###
        shutil.move("scss/libraryroot.custom.scss", "scss/libraryroot.custom.scss.backup2")
        shutil.move("scss/libraryroot.custom.temp.scss", "scss/libraryroot.custom.scss")
            
    except:
        print("Error removing existing themes.", file=sys.stderr)
        print_traceback()
    
    #print("TODO")


'''
config_replacements = {'--FontSize: 15px;' : '--FontSize: 13px;',
                       '--YourLibraryName: "YOUR LIBRARY"' : '--YourLibraryName: "HOME"',
                       '--LetterSpacing: 3px' : '--LetterSpacing: 0px',
                       '--ButtonPlayHover: #70d61d;' : '--ButtonPlayHover: var^(--libraryhome^)^;',
                       '--ButtonPlayHover2: #01a75b;' : '--ButtonPlayHover2: var^(--libraryhome^)^;',
                       '--ButtonInstallHover: #47bfff;' : '--ButtonInstallHover: var^(--libraryhome^)^;',
                       '--ButtonInstallHover2: #1a44c2;' : '--ButtonInstallHover2: var^(--libraryhome^)^;'
                       }
'''

def steam_library_compat_config():
    
    try:
        if not os.path.isfile("themes/config.css"):
            shutil.copy2("themes/config.css.original", "themes/config.css")
            '''
            with open("themes/config.css", "r", newline='', encoding="UTF-8") as f, \
                 open("themes/config.temp.css", "w", newline='', encoding="UTF-8") as f1:

                for line in f:   
                    f1.write(line)

                f.close()
                f1.close()
               
                shutil.move("themes/config.css", "themes/config.css.backup")
                shutil.copy2("themes/config.temp.css", library_dir() + "/" + "config.css")
                shutil.move("themes/config.temp.css", "themes/config.css")
            '''
        shutil.copy2("themes/config.css", library_dir() + "/" + "config.css")
        print("themes/config.css copied to: " + library_dir())
    except FileNotFoundError:
        print("config.css not found", file=sys.stderr)
        print_traceback()
    
    pass

### END 
### 



###
### JS functions (fixes.txt)
### Load state of JS Fixes (enabled, disabled) from file
def load_js_fixes():
    js_fixes_filename = 'fixes.txt'
    try:
        fixesdata = {}
        special_fixesdata = {}
        fixname = ""
        readfix = 0
        sectionhead = 0
        state = 3 #0 = disabled(commented out), 1 = enabled, 2 = mixed, starting

        with open(js_fixes_filename, newline='', encoding="UTF-8") as infile:
            for line in infile:
                if re.match("### ===.*===", line):
                    readfix = 1
                    sectionhead = 1
                    fixname = line
                    fixname = re.sub("### ===|===", "", line).strip()
                elif line.strip(' ') == OS_line_ending():
                    readfix = 0
                if readfix == 1 and sectionhead == 0:
                    if line.lstrip()[:3] == "###":
                        state = 2 if state == 1 else 0 #set state as mixed if state is already enabled
                    else:
                        state = 1
                    if state == 2:
                        print("Mixed enabled/disabled tweak found in fix:", file=sys.stderr)
                        print("  " + fixesname, file=sys.stderr)
                        print("Please check the lines in fixes.txt and see if\n"\
                              "they are all commented out (with ###) or enabled (without ###).", file=sys.stderr)
                    fixesdata[fixname] = str(state)
                    (key, val) = line.rstrip().split("  ") #validation
                    ### special fixes data, line to look out for has n = [number] in it
                    if "Change Game Image Grid Sizes" in fixname and re.search("n = ([0-9]+)", line):
                        line_segments = line.split("  ")
                        sizes_dict = {}
                        sizes = ["Small", "Medium", "Large"]
                        size_values = re.findall("n = ([0-9]+)", line_segments[1])
                        for i, value in enumerate(size_values):
                            sizes_dict[sizes[i]] = value
                        special_fixesdata[fixname] = sizes_dict
        
                elif readfix == 0:
                    state = 0
                sectionhead = 0               
        infile.close()
        
        print("Loaded JS Tweaks. " + "(" + js_fixes_filename + ")")
    except ValueError:
        print("(" + js_fixes_filename + ") Problem in line format from line: " + line + \
              "Is the line missing a double space?", file=sys.stderr)
    except FileNotFoundError:
        print("JS Tweaks file, '" + js_fixes_filename + "' not found", file=sys.stderr)
    except Exception as e:
        print("Error loading JS Tweaks (" + js_fixes_filename + ") from line: " + line, file=sys.stderr)
        print_traceback()
    return fixesdata, special_fixesdata
    
    

def write_js_fixes(fixesdata, special_fixesdata):
    try:
        #print("~0~~")
        #print(fixesdata)
        writefix = 0
        current_fixname = ""
        sectionhead = 0
        with open('fixes.txt', "r", newline='', encoding="UTF-8") as f, \
             open("fixes.temp.txt", "w", newline='', encoding="UTF-8") as f1:
            for line in f:
                for fixname in fixesdata:
                    if fixname in line:
                        current_fixname = fixname
                        sectionhead_line = "### === " + fixname + " ==="
                        f1.write(sectionhead_line + OS_line_ending())
                        writefix = 1
                        sectionhead = 1
                if line.strip(' ') == OS_line_ending():
                    writefix = 0
                    f1.write(OS_line_ending())
                if writefix == 1 and sectionhead == 0:
                    ### special fixes data
                    if "Change Game Image Grid Sizes" in current_fixname:
                        line_segments = line.split("  ")

                        sizes = ["Small", "Medium", "Large"]
                        line_segments[1] = re.sub("n = ([0-9]+)", "n = AAA", line_segments[1])
                        #print(line_segments[1])
                        for key in sizes:
                            #print(special_fixesdata[current_fixname][key])
                            #print(special_fixesdata)
                            line_segments[1] = line_segments[1].replace("AAA", special_fixesdata[current_fixname][key], 1)
                        #print(line_segments[1])

                        line = "  ".join(line_segments)
                        #print(line)
                    #print("~C!~~~")
                    #print(current_fixname + "   ")
                    #print(fixesdata[current_fixname])                    
                    if line.lstrip()[:3] == "###":
                        if fixesdata[current_fixname] == '1':
                            #print("STRIP COMMENT AND ENABLE")
                            #print(line.lstrip().split("###")[1])
                            f1.write(line.lstrip().split("###")[1])
                        else:
                            f1.write(line)
                            pass
                    else:
                        #print(fixesdata[current_fixname])
                        if fixesdata[current_fixname] == '0':
                            #print("ADD COMMENT AND DISABLE")
                            f1.write("###" + line.lstrip())
                        else:
                            f1.write(line)
                            pass
                    
                sectionhead = 0
                    
        #print(fixesdata)
        f.close()
        f1.close()
        ###
        shutil.move("fixes.txt", "fixes.txt.backup")
        shutil.move("fixes.temp.txt", "fixes.txt")
                    
    except FileNotFoundError:
        print("JS Tweaks file, 'fixes.txt' not found", file=sys.stderr)
    except Exception as e:
        print("Error writing JS Tweaks (fixes.txt) from line: " + line, file=sys.stderr)
        print_traceback()
                    
def refresh_steam_dir():
    try:
        if os.path.isfile(library_dir() + "/" + "libraryroot.custom.css"):# and os.stat(library_dir() + "/" + "libraryroot.custom.css").st_size > 15:
            if os.path.isfile(library_dir() + "/" + "libraryroot.custom.css.backup"):
                print("Existing libraryroot.custom.css code detected.")
                shutil.copy2(library_dir() + "/" + "libraryroot.custom.css", library_dir() + "/" + "libraryroot.custom.css.backup2")
                print("Backed up steamui/libraryroot.custom.css to steamui/libraryroot.custom.css.backup2")
            else:
                shutil.copy2(library_dir() + "/" + "libraryroot.custom.css", library_dir() + "/" + "libraryroot.custom.css.backup")
                print("backed up steamui/libraryroot.custom.css to steamui/libraryroot.custom.css.backup")
            shutil.copy2("libraryroot.custom.css", library_dir() + "/" + "libraryroot.custom.css")
        elif not os.path.isfile(library_dir() + "/" + "libraryroot.custom.css"):
            shutil.copy2("libraryroot.custom.css", library_dir() + "/" + "libraryroot.custom.css")
        print("File " + "libraryroot.custom.css" + " written to " + library_dir())
        
        #shutil.copy2(library_dir() + "/licenses.txt", library_dir() + "/licenses.txt.copy")
        #os.remove(library_dir() + "/licenses.txt.copy")
        f = open(library_dir() + "/refresh_dir.txt", "w", newline='', encoding="UTF-8")
        f.close()
        os.remove(library_dir() + "/refresh_dir.txt")
    except:
        print("Unable to copy libraryroot.custom.css to Steam directory.", file=sys.stderr)
        print_traceback()
    

def clean_slate_css():    
    try:
        f = open(library_dir() + "/" + "libraryroot.empty.css", "w", newline='', encoding="UTF-8")
        #f.write(OS_line_ending())
        f.close()
        if os.path.isfile(library_dir() + "/" + "libraryroot.custom.css"):
            shutil.move(library_dir() + "/" + "libraryroot.custom.css", library_dir() + "/" + "libraryroot.custom.css.backup")
        shutil.move(library_dir() + "/" + "libraryroot.empty.css", library_dir() + "/" + "libraryroot.custom.css")
        print("libraryroot.custom.css in Steam directory emptied out, backup at libraryroot.custom.css.backup")
        shutil.copy2("themes/config.css.original", library_dir() + "/" + "config.css")
        
    except:
        print("Was not able to completely reset libraryroot.custom.css.", file=sys.stderr)
        print_traceback()

def clear_js_working_files():
    try:
        files_to_remove = ["library.js", "libraryroot.js", "libraryroot.beaut.js"]
        for file in files_to_remove:
            w_file = Path(file)
            w_file.unlink(missing_ok=True)
            print("Local " + file + " deleted.")
    except:
        print("Was not able to remove " + file, file=sys.stderr)
        print_traceback()
        
### Auto-update functions

def create_session():
    try:
        username = ''
        token = '5d6ecfc25f9f2b5cb1c1d88b316bd0bf11b0a101'
        session = requests.Session()
        session.auth = (username, token)
        return session
    except:
        print("Unable to request Github API session.", file=sys.stderr)
        print_traceback()
        
def get_small_update_file_list():
    try:
        list_filename = 'small_update_file_list.json'
        branch = 'dev'
        session = create_session()        
        response = session.get('https://raw.githubusercontent.com/Jonius7/SteamUI-OldGlory/' + \
                               branch + "/" + list_filename)
        return response.json()
    except json.decoder.JSONDecodeError as e:
        print("Error in update filelist JSON format.\nThis is an issue with " + list_filename + " on Github.", file=sys.stderr)
        print_traceback()
    except:
        print("Unable to load update filelist", file=sys.stderr)
        print_traceback()

def check_new_commit_dates(json_data):
    try:
        file_dates = {}
        file_list = get_small_update_file_list()
        for f in file_list:
            for pathname in file_list[f]:
                session = create_session()
                response = session.get("https://api.github.com/repos/jonius7/steamui-oldglory/commits?path=" + \
                                       pathname + "&page=1&per_page=1")
                #print(json_data["lastPatchedDate"] < response.json()[0]["commit"]["committer"]["date"])
                
                if json_data["lastPatchedDate"] < response.json()[0]["commit"]["committer"]["date"]:
                    print(f.replace("_", " ") + " found: " + pathname)
                #print(pathname + " | " + response.json()[0]["commit"]["committer"]["date"])
                #print(response.json())
                #file_dates {pathname}
                #if 
    except:
        print("Unable to check for latest small update files on Github.", file=sys.stderr)
        print_traceback()

def update_json_last_patched_date():
    print("TODO")
