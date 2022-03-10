'''
backend.py
Handles the backend for applying CSS and checking for updates

libraries needed: requests, requests_oauthlib, libsass
'''

import platform
import os
import sys
import subprocess
import shutil
import traceback
import re
from pathlib import Path
import configparser
import json
import sass
from datetime import datetime, timezone
import requests
from requests_oauthlib import OAuth1Session
from hashlib import sha1
import time

import defaults
import js_tweaker
import backend
import js_manager

##########################################
### CONSTANTS

OS_TYPE = platform.system()
if OS_TYPE == "Windows":
    import winreg

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
            "desc" : "Corresponds with JavaScript tweak - Home Page Grid Spacing."},
        "--RemoveGameHover" : {
            "default" : "block",
            "current" : "block",
            "options": {"block", "none"},
            "desc" : "Set to none to remove game preview box when hovering over game."}
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
            "desc" : "Set left to swap columns."},
        "--AchievementsClickHighlight" : {
            "default" : "appdetailsoverview_HighlightMe_25jnp",
            "current" : "Highlight_opacity",
            "options": {"appdetailsoverview_HighlightMe_25jnp", "Highlight_opacity", "Highlight_border", "disabled"},
            "desc" : "Options: Highlight_opacity Highlight_border. Set to disabled to disable."}
        },
    "Game Page Elements" : {
        "--RecommendGame" : {
            "default" : "block",
            "current" : "block",
            "options": {"block", "none"},
            "desc" : "Set to none to hide 'Recommond this game' box on game page."},
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

ROOT_MAP = {"start" : ["Configurable variables", ":root {"],
            "end" : ["}", "======"]
            }

PATCHED_TEXT = "/*patched*/"

### [END OF] CONSTANTS
##########################################


##########################################
### GENERAL UTILITY Functions

def OS_line_ending():
    '''
    UTILITY: Returns line ending for Windows, Mac, Linux.
    '''
    if OS_TYPE == "Windows":
        return "\r\n"
    elif OS_TYPE ==  "Darwin":
        return "\n"
    elif OS_TYPE ==  "Linux":
        return "\n"

# could use testing
def OS_open_file(path):
    '''
    UTILITY: Returns file explorer path for Windows, Mac, Linux.
    '''
    try:
        if os.path.exists(path):
            if OS_TYPE == "Windows":
                subprocess.Popen(["explorer", path])
            elif OS_TYPE ==  "Darwin":
                subprocess.Popen(["open", path])
            elif OS_TYPE ==  "Linux":
                subprocess.Popen(["xdg-open", path])
            print("Opened: " + path)
        else:
            print("Path " + path + " does not exist.", file=sys.stderr)
    except:
        print_traceback()
    
def library_dir():
    '''
    UTILITY: Returns Steam library path (/steamui) for Windows, Mac, Linux.
    '''
    try:
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
    except:
        print("Steam Library directory not found. Is Steam installed/has been run under this User?", file=sys.stderr)
        print_traceback()

def print_traceback():
    '''
    UTILITY: Prints error traceback.
    '''
    print("~~~~~~~~~~~~~~~~~~~~")
    print(traceback.format_exc(), end='', file=sys.stderr)
    print("~~~~~~~~~~~~~~~~~~~~")

def help():
    '''
    UTILITY: Prints a list of functions and their descriptions.
    '''
    l = []
    for key, value in globals().items():
        if callable(value) and value.__module__ == __name__:
            l.append(key)
            print("{0}() {1}".format(key, globals()[key].__doc__))
    #for item in l:
        
    
def get_file_hash(filepath):
    '''
    UTILITY: Returns the git SHA hash of a file.
    '''
    try:
        with open(filepath, 'r', encoding="UTF-8") as f, \
            open(filepath + ".temp", 'w', encoding="UTF-8", newline='\n') as f1:
            f1.writelines(f.readlines())
        f.close()
        f1.close()

        filesize_bytes = os.path.getsize(filepath + ".temp")

        s = sha1()
        s.update(b"blob %u\0" % filesize_bytes)
        
        with open(filepath + ".temp", 'rb') as g:
            s.update(g.read())
        g.close()

        if os.path.exists(filepath + ".temp"):
            os.remove(filepath + ".temp")
        
        return s.hexdigest()
    except:
        print("Unable to get hash of file: " + filepath, file=sys.stderr)
        print_traceback()
        
def get_file_hash_b(filepath):
    '''
    UTILITY: Returns the git SHA hash of a file.
    '''
    BUF_SIZE = 65536
    try:
        pass
        
    except:
        print("Unable to get hash of file: " + filepath, file=sys.stderr)
        print_traceback()
    

### Check CSS Patched
def is_css_patched(filename="5.css"):
    '''
    UTILITY: Returns whether the Steam Library CSS has been patched.
    '''
    patched = False
    filepath = library_dir() + "/css/" + filename    
    try:
        with open(filepath, newline='', encoding="UTF-8") as f:
            first_line = f.readline()
        if PATCHED_TEXT in first_line:
            patched = True
        else:
            pass
            #print("css\libraryroot.css not patched.", file=sys.stderr)
        f.close()
    except FileNotFoundError:
        print("File at " + filepath + " (previously known as libraryroot.css) not found.", file=sys.stderr)
    except:
        print("Error occured while trying to find patched CSS css/" + filename, file=sys.stderr)
        print_traceback()
    return patched

### datetime
def get_remote_datetime(timezone=timezone.utc):
    '''
    UTILITY: Return datetime string in timezone (default UTC).
    '''
    date = datetime.now(timezone)
    date_f = date.strftime("%Y-%m-%dT%H:%M:%SZ")
    return date_f

def get_local_datetime():
    '''
    UTILITY: Return datetime string in local time.
    '''
    date = datetime.now()
    date_f = date.strftime("%Y-%m-%dT%H:%M:%SZ")
    return date_f

# of the format "%Y-%m-%dT%H:%M:%SZ"
def datetime_string_to_obj(date_string):
    '''
    UTILITY: Convert datetime string to object.
    '''
    return datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%SZ")


### [END OF] GENERAL UTILITY Functions
##########################################


##########################################
### JSON Functions
def get_json_data(json_data_filename = 'old_glory_data.json'):
    '''
    JSON: load data from JSON file and return it as an object
    '''
    try:
        with open(json_data_filename, encoding="UTF-8") as f:
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

def write_json_data(json_data):
    '''
    '''
    json_data_filename = 'old_glory_data.json'
    try:
        with open(json_data_filename, "r", newline=OS_line_ending(), encoding="UTF-8") as f, \
             open(json_data_filename + ".temp", "w", newline=OS_line_ending(), encoding="UTF-8") as f1:
            w_json = json.dump(json_data, f1, indent="\t")
        f.close()

        shutil.move(json_data_filename, json_data_filename + ".backup")
        shutil.move(json_data_filename + ".temp", json_data_filename)
            
    except:
        print("Error writing/updating " + json_data_filename, file=sys.stderr)
        print_traceback()

        
### [END OF] JSON Functions
##########################################
        

##########################################
### CONFIG Functions

def load_config(config_filename = "oldglory_config2.cfg"):
    config_dict = {}
    if not os.path.isfile(config_filename) :
        print("Config file " + config_filename + " not found. Creating copy with default options.", file=sys.stderr)
        write_config(defaults.DEFAULT_CONFIG)
        return defaults.DEFAULT_CONFIG
    else:
        config = configparser.ConfigParser()
        config.optionxform = str
        config.read(config_filename)
        for section in config.sections():
            options = config.options(section)
            temp_dict = {}
            for option in options:
                temp_dict[option] = config.get(section, option)
            config_dict[section] = temp_dict
        return config_dict

def test_config(config_filename = "oldglory_config2.cfg"):
    config = configparser.ConfigParser()
    config.optionxform = str
    config.read(config_filename)
    return config

def write_config(config_dict = defaults.DEFAULT_CONFIG):
    config = configparser.ConfigParser()
    config.optionxform = str
    for section in config_dict:
        config[section] = config_dict[section]
    #print(config.sections())
    #print(config.options("Main_Settings"))
    with open("oldglory_config2.cfg", "w", newline='', encoding="UTF-8") as config_file:
        config.write(config_file)
    config_file.close()
    print("Config file written.")

### [END OF] CONFIG Functions
##########################################


##########################################
### SETTINGS Functions
###   GUI Checkboxes
###   Need to change logic to cover "unchecking" options

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
        if "InstallWithLibraryTheme" in settings: #6
            validated_settings.extend(["InstallWithLibraryTheme"])
    #print(validated_settings)
    return validated_settings

### [END OF] SETTINGS Functions
##########################################


##########################################
### CSS Functions
###   (scss/libraryroot.custom.scss)
###   if/for loops could be reduced

SETTING_MAP = {
    "InstallCSSTweaks" : "",
    "EnablePlayButtonBox" : {"filename" : "module_playbarbox"},
    "EnableVerticalNavBar" : {"filename" : "module_verticalnavbar"},
    "EnableClassicLayout" : {"filename" : "module_classiclayout"},
    "LandscapeImages" : {"filename" : "module_landscapegameimages"},
    "InstallWithLibraryTheme" : "",
    "ClassicStyling" : {"filename" : "classic"},
    "ThemeSelected" : ""
}
       
def write_css_settings(settings): 
    try:
        with open("scss/libraryroot.custom.scss", "r", newline='', encoding="UTF-8") as f, \
             open("scss/libraryroot.custom.temp.scss", "w", newline='', encoding="UTF-8") as f1:

            import_prefix = '@import "./'
            themes_prefix = '@import "../themes/'
            start_comment = '//'
            modify = 0
            for line in f:
                #if themes_prefix not in line or import_prefix in line:
                if import_prefix in line:
                    for setting in settings:
                        if 'filename' in SETTING_MAP[setting]:
                            if import_prefix + SETTING_MAP[setting]['filename'] in line:
                                if line.startswith(start_comment):
                                    if settings[setting]["value"] == "1" and setting in settings \
                                        and settings[setting]["state"] == "normal":
                                        modify = 1
                                        f1.write(LineParser.remove_start_comment(start_comment, line))
                                else:    
                                    if settings[setting]["value"] == "0":
                                        modify = 1
                                        f1.write(LineParser.add_start_comment(start_comment, line))
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
        print("Error enabling/disabling CSS modules,\nat " + line, file=sys.stderr)
        print_traceback()

class LineParser():
         
    @staticmethod 
    def remove_start_comment(start_comment, line):
        #strips start_comment and any spaces before line
        return line.split(start_comment)[1].lstrip()
    
    @staticmethod
    def add_start_comment(start_comment, line):
        #Concatenates start_comment to line (space in between)
        return start_comment + " " + line

def compile_css(json_data):
    '''
    Compiles libraryroot.custom.css from /scss directory
    Adds variables.css
    '''
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
                        #load options for dropdown (currently unused)
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

def css_line_parser(line):
    '''
    Parses one line of CSS file into dictionary values
    '''
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
#from css_config dictionary to an array of lines of CSS to be written
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


### [END OF] CSS Functions
##########################################


##########################################
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


def steam_library_compat_config(overwrite=0):
    try:
        if not os.path.isfile("themes/config.css"):                             # if config.css in OldGlory themes/ doesn't exist
            shutil.copy2("themes/config.css.original", "themes/config.css")     # make a copy from config.css.original
            print("created themes/config.css from themes/config.css.original")
        if not os.path.isfile(library_dir() + "/" + "config.css"):
            overwrite = 1
        if overwrite == 1:
            shutil.copy2("themes/config.css", library_dir() + "/" + "config.css")   # copy config.css from OldGlory themes/ to steamui/
            print("themes/config.css copied to: " + library_dir() + "/" + "config.css")
        print("If you encounter visual errors, try Apply config.css in Advanced Options", file=sys.stderr)
        refresh_steam_dir()
    except FileNotFoundError:
        print("config.css not found", file=sys.stderr)
        print_traceback()
    pass

### [END OF] APPLY CSS THEME Functions
##########################################


##########################################
### JS Functions
def load_js_tweaks(config_dict, filename="js_tweaks.yml"):
    pass
    fixesdata = {}
    valuesdata = {}
    y = js_tweaker.YamlHandler(filename)
    #c = js_manager.ConfigJSHandler(y.data, config_dict)
    
    for config in config_dict["JS_Settings"]:
        #print("way")
        #if y.data[config]:
        #print(y.data[config])
        fixesdata[config] = str(config_dict["JS_Settings"][config])
        if config in y.data:
            if "values" in y.data[config]:
                #print(config)
                for value in y.data[config]["values"]:
                    if value in config_dict["JS_Values"]:
                        if config in valuesdata:
                            valuesdata[config].update({value: config_dict["JS_Values"][value]})
                        else:
                            valuesdata[config] = {value: config_dict["JS_Values"][value]}
    return fixesdata, valuesdata


### fixes.txt
### Load state of JS Fixes (enabled, disabled) from file fixes.txt
def load_js_fixes_OLD():
    js_fixes_filename = 'fixes.txt'
    try:
        fixesdata = {}
        special_fixesdata = {}
        fixname = ""
        readfix = 0
        sectionhead = 0
        state = 3 #0 = disabled(commented out), 1 = enabled, 2 = mixed, starting

        with open(js_fixes_filename, newline='', encoding="UTF-8") as infile:
            for a, line in enumerate(infile):
                if line.strip(' ') == OS_line_ending():
                    readfix = 0
                elif re.match("### ===.*===", line):
                    readfix = 1
                    sectionhead = 1
                    fixname = line
                    fixname = re.sub("### ===|===", "", line).strip()
                if readfix == 1 and sectionhead == 0:
                    if line.lstrip()[:3] == "###":
                        state = 2 if state == 1 else 0 #set state as mixed if state is already enabled
                    else:
                        state = 1
                    if state == 2:
                        print("Mixed enabled/disabled tweak found in fix:", file=sys.stderr)
                        print("  " + fixname, file=sys.stderr)
                        print("Please check the lines in " + js_fixes_filename + " and see if\n"\
                              "they are all commented out (with ###) or enabled (without ###).\n", file=sys.stderr)
                    fixesdata[fixname] = str(state)
                    (key, val) = line.rstrip().split("  ") #validation
                    ### special fixes data, line to look out for has n = [number] in it
                    ### could rewrite in the future
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
        print("(" + js_fixes_filename + ") Problem in format of Line " + str(a) + ": " + line + \
              "Is the line missing a double space?", file=sys.stderr)
        print_traceback()
    except FileNotFoundError:
        print("JS Tweaks file, '" + js_fixes_filename + "' not found", file=sys.stderr)
    except Exception as e:
        print("Error loading JS Tweaks (" + js_fixes_filename + ") from line: " + line, file=sys.stderr)
        print_traceback()
    return fixesdata, special_fixesdata
    

def write_js_tweaks(js_config, values_config):
    pass

    

def write_js_fixes_OLD(fixesdata, special_fixesdata):
    try:
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

### [END OF] JS Functions
##########################################


##########################################
### STEAM DIRECTORY AND CLEAR Functions

                    
def backup_libraryroot():
    try:
        local_libraryroot_custom_css = "libraryroot.custom.css"
        libraryroot_custom_css = library_dir() + "/" + "libraryroot.custom.css"
        libraryroot_custom_css_backup = library_dir() + "/" + "libraryroot.custom.css.backup"
        libraryroot_custom_css_backup2 = library_dir() + "/" + "libraryroot.custom.css.backup2"
        
        if os.path.isfile(libraryroot_custom_css):
            print("Existing libraryroot.custom.css code detected.")
            if os.path.isfile(libraryroot_custom_css_backup):
                shutil.copy2(libraryroot_custom_css, libraryroot_custom_css_backup2)
                print("Backed up steamui/libraryroot.custom.css to steamui/libraryroot.custom.css.backup2")
            else:
                shutil.copy2(libraryroot_custom_css, libraryroot_custom_css_backup)
                print("backed up steamui/libraryroot.custom.css to steamui/libraryroot.custom.css.backup")
            shutil.copy2(local_libraryroot_custom_css, libraryroot_custom_css)
        elif not os.path.isfile(libraryroot_custom_css):
            shutil.copy2(local_libraryroot_custom_css, libraryroot_custom_css)
        print("File " + local_libraryroot_custom_css + " written to " + libraryroot_custom_css)
    except:
        print("Unable to copy libraryroot.custom.css to Steam directory.", file=sys.stderr)
        print_traceback()

def refresh_steam_dir():
    try:
        #refresh steam library
        f = open(library_dir() + "/refresh_dir.txt", "w", newline='', encoding="UTF-8")
        f.close()
        if os.path.exists(library_dir() + "/refresh_dir.txt"):
            os.remove(library_dir() + "/refresh_dir.txt")
    except:
        print("Unable to refresh Steam directory.", file=sys.stderr)
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
        files_to_remove = ["library.js", "library.beaut.js", "libraryroot.js", "libraryroot.beaut.js"]
        for file in files_to_remove:
            w_file = Path(file)
            w_file.unlink(missing_ok=True)
            print("Local " + file + " deleted.")
    except:
        print("Was not able to remove " + file, file=sys.stderr)
        print_traceback()

### [END OF] STEAM DIRECTORY AND CLEAR Functions
##########################################


##########################################
### AUTO-UPDATE functions
BRANCH = "master"
        
def create_session():
    try:
        username = ''
        token = unscramble_token('knqcpp7j7vqg1z1c2jovzwjocpp27o2oapvzwtnp')
        session = requests.Session()
        session.auth = (username, token)
        return session
    except:
        print("Unable to request Github API session.", file=sys.stderr)
        print_traceback()

def unscramble_token(scrambled_token):
    charset = '0123456789abcdef'
    keyset = '7oqngcwvjtka21pz'
    key_indices = [keyset.index(k) for k in scrambled_token]
    plain_token = ''.join(charset[keyIndex] for keyIndex in key_indices)
    return plain_token


# returns a dictionary in the form: {'Update_Type1': ['file1', 'file2', ...],  'Update_Type2': ['file1', 'file2', ...], ... }
def get_small_update_file_list():
    try:
        list_filename = 'small_update_file_list.json'
        session = create_session()        
        response = session.get('https://raw.githubusercontent.com/Jonius7/SteamUI-OldGlory/' + \
                               BRANCH + "/" + list_filename)
        return response.json()
    except json.decoder.JSONDecodeError as e:
        print("Error in update filelist JSON format.\nThis could be an issue with:\n" \
              "- " + list_filename + " on Github.\n" \
              "- Too many Github API requests (access token could have been removed)", file=sys.stderr)
        print_traceback()
    except:
        print("Unable to load update filelist", file=sys.stderr)
        print_traceback()


#returns a list of files from small_update_file_list that are newer on Github than the last patched date (found in old_glory_data.json)
# returns file_dates
# a dictionary in the form: {'Update_Type1': ['file1': 'date1', 'file2': 'date2', ...],
#                                    'Update_Type2': ['file1': 'date1', 'file2': 'date2', ...],
# date is a string in the format "%Y-%m-%dT%H:%M:%SZ" aka "YYYY-mm-ddTHH:MM:SSZ"
def check_new_commit_dates(json_data):
    try:
        file_dates = {}
        file_list = get_small_update_file_list()
        
        '''
        #use local version of file for debugging purposes
        with open('small_update_file_list.json') as f:
            file_list = json.load(f)
        f.close()
        '''
        
        for k, v in file_list.items():
            file_dates_item = {}
            for pathname in file_list[k]:
                session = create_session()
                response = session.get("https://api.github.com/repos/jonius7/steamui-oldglory/commits?path=" + \
                                       pathname + "&page=1&per_page=1&sha=" + BRANCH)
                #print(json_data["lastPatchedDate"] < response.json()[0]["commit"]["committer"]["date"])

                # if commit date is newer than last patched dated
                commit_date = response.json()[0]["commit"]["committer"]["date"]
                
                if json_data["lastPatchedDate"] < commit_date:
                    #print(k.replace("_", " ") + " found: " + pathname)
                    file_dates_item[pathname] = commit_date
                #print(pathname + " | " + response.json()[0]["commit"]["committer"]["date"])
                #print(response.json())
                #if
            file_dates.update({k : file_dates_item})
        return file_dates
    except AttributeError as e:
        print("No commit dates found", file=sys.stderr)
    except:
        print("Unable to check for latest small update files on Github.", file=sys.stderr)
        print_traceback()

#returns a list of strings
def format_file_dates_to_strings(file_dates):
    messages = []
    for k, v in file_dates.items():
        if len(v) > 0:
            messages.append("--- " + k.replace("_", " ") + " found: ---")
        for fp in v:
            messages.append(fp)
    return messages
        

### only for root directory on repo
def is_file_or_directory(name, contents):
    for i, data in enumerate(contents):
        if data["name"] == name:
            #print("AHA " + name)
            return contents[i]["type"]
        
def update_json_last_patched_date(json_data):
    #print(json_data)
    json_data["lastPatchedDate"] = get_remote_datetime()
    #print(json_data)
    write_json_data(json_data)

### file management functions as part of auto-update
### file_dates - dictionary of filenames with their dates
### return dictionary of files that are different/needing download
### a dictionary in the form: {'Update_Type1': ['file1': 'date1', 'file2': 'date2', ...],
#                              'Update_Type2': ['file1': 'date1', 'file2': 'date2', ...],
def hash_compare_small_update_files(file_dates, json_data):
    try:
        files_to_download = {}
        #
        #start_time = time.time()
        session = create_session()
        response = session.get("https://api.github.com/repos/jonius7/steamui-oldglory/contents?ref=" + BRANCH)
        root_contents = response.json()
        #print("--- %s seconds ---" % (time.time() - start_time))
        
        for k, v in file_dates.items():
            updatetype_files = []
            for filename in v: # for each filename in Update type
                file_or_directory = is_file_or_directory(filename, root_contents)
                #print(filename)
                if file_or_directory == "dir": #if directory
                    contents = get_repo_directory_contents(filename) # github /contents
                    for filedata in contents:
                        #print(filedata["name"], end='\t')
                        
                        local_filepath = filename + "/" + filedata["name"]
                        #print(local_filepath)
                        if os.path.exists(local_filepath):
                            #if local hash != remote hash
                            # Need to change hardcoding these filenames
                            if (get_file_hash(local_filepath) != filedata["sha"] and
                                 local_filepath != "scss/libraryroot.custom.scss" and
                                 local_filepath != "scss/_custom_module1.scss" and
                                 local_filepath != "scss/_custom_module2.scss"):                
                                #print("Different file hashes " + local_filepath)
                                #print(local_filepath + " | " + get_file_hash(local_filepath) + "  |  " + filedata["sha"])
                                print("New Version | " + local_filepath)
                                updatetype_files.append(local_filepath)
                            #print("", end="")
                        else:
                            print("File at " + local_filepath + " exists on remote but not locally")
                            updatetype_files.append(local_filepath)
                elif file_or_directory == "file": #if file
                    date_obj_remote = datetime_string_to_obj(file_dates[k][filename])
                    date_obj_local = datetime_string_to_obj(json_data["lastPatchedDate"])
                    #print(date_obj_remote)
                    #print(date_obj_local)
                    #print("~~~~~~~~~~(~")
                    if date_obj_remote > date_obj_local:
                        #print(filename + " | " + get_file_hash(filename))
                        print("New Version | " + filename)
                        updatetype_files.append(filename)
            files_to_download[k] = updatetype_files

        '''
        #print("libraryroot gets different rules")
        session = create_session()
        response = session.get(
            "https://api.github.com/repos/jonius7/steamui-oldglory/commits?path=" + local_filepath)
        #print(response.json())
        date = response.json()[0]["commit"]["committer"]["date"]
        date_obj_remote = datetime_string_to_obj(date)
        date_obj_local = datetime_string_to_obj(json_data["lastPatchedDate"])
        if date_obj_remote > date_obj_local:
            print("ADDED " + local_filepath)
            files_to_download.append(local_filepath)
        #print(date_obj_remote)
        #print(date_obj_local)
        '''

                        
        return files_to_download
    except:
        print("Unable to compare file hashes for small update files.", file=sys.stderr)
        print_traceback()

def files_to_download_dtol(files_dict):
    files_list = []
    for k, v in files_dict.items():
        for filename in v:
            files_list.append(filename)
    return files_list
              
def get_repo_directory_contents(directory_name):
    session = create_session()
    response = session.get("https://api.github.com/repos/jonius7/steamui-oldglory/contents/" + \
                           directory_name + "?ref=" + BRANCH)
    return response.json()

# moves files in filelist to backups/[YYYY-mm-dd HH:MM:ss]
# filelist = list of strings ['filepath1', 'filepath2']
def backup_old_versions(filelist):
    try:
        backups_folder = "backups"
        local_time = get_local_datetime().replace("T", " ").replace(":", "-").replace("Z", "")
        
        backup_path = os.path.join(backups_folder, local_time)
        if not os.path.exists(backup_path):
            os.makedirs(backup_path)
        for filepath in filelist:
            sp_filepath = filepath.split("/")
            sp_dir = sp_filepath[:-1]
            filedir = os.path.join('', *sp_dir)
            if not os.path.exists(os.path.join(backup_path, filedir)):
                os.makedirs(os.path.join(backup_path, filedir))
            if os.path.exists(filepath):
                shutil.move(filepath, os.path.join(backup_path, filedir, sp_filepath[-1]))
                print("File " + sp_filepath[-1] + " moved to " + os.path.join(backup_path, filedir, sp_filepath[-1]))
    except:
        print("Unable to backup old versions of small update files.", file=sys.stderr)
        print_traceback()

### in the future could try to preserve date modified (optional)
def download_file(filepath, branch=BRANCH):
    try:
        url = 'https://raw.githubusercontent.com/Jonius7/SteamUI-OldGlory/'
        r = requests.get(url + branch + "/" + filepath, allow_redirects=True)
        if not os.path.exists(filepath):
            if r.ok:
                # split
                dirs = filepath.split("/")
                if len(dirs) == 2 and not os.path.exists(dirs[0]):
                    os.makedirs(dirs[0])            
                #open(filepath, 'wb').write(r.context)
                open(filepath, 'w', encoding="UTF-8").write(r.text)
                print("File " + filepath + " downloaded.")
            else:
                print("Invalid request URL")
        else:
            print("File at " + filepath + " already exists!")
    except:
        print("Unable to download file " + str(filepath), file=sys.stderr)
        print_traceback()

### [END OF] AUTO-UPDATE Functions
##########################################
