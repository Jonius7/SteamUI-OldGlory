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
import urllib.request
import sass
from datetime import datetime, timezone
import requests
from requests_oauthlib import OAuth1Session
import hashlib
from pathlib import Path
#from playwright.sync_api import sync_playwright, Playwright, Page
import asyncio
import pyppeteer
#import urllib3
#import psutil

##########################################
### CONSTANTS

OS_TYPE = platform.system()
if OS_TYPE == "Windows":
    import winreg

DEFAULT_CONFIG = {
    "Filepaths" : {
        "SteamLibraryPath" : "",
        "PatcherPath" : "",
        "InstallMode" : "SFP/Millennium",
    },
    "Main_Settings" : {
        "InstallCSSTweaks" : "1",
        "EnablePlayButtonBox" : "0",
        "EnableVerticalNavBar" : "0",
        "EnableClassicLayout" : "0",
        "LandscapeImages" : "0",
        "InstallWithLibraryTheme" : "0",
        "ThemeSelected" : "Crisp Cut",
        "ClassicStyling" : "0",
        "HomeButton" : "1",
    },
    "JS_Settings" : {
        "HomePageGridSpacing" : "1",
        "MoreScreenshotsAndDLC" : "1",
        "HoverPositionFix" : "1",
        "ScrollPastAddShelf" : "1",
        "ChangeGameImageGridSizes" : "1",
        "VerticalNavBar" : "1",
        "LandscapeGameImages" : "1",
        "StopWhatsNewLoad" : "0",
        "SmootherHomePageScrolling" : "1",
        "GamePropertiesWindowSize" : "1",
        "StickyBackgroundImage" : "1",
        "PressEnterToLaunchGames" : "1",
        "ExpandShowMoreDetails" : "0",
        "DontLoadHomeGameImages" : "0",
        "DontLoadGamePageSections" : "0",
    } 
}


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
            "current" : "0",
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
        
        "--DLCAvailableContent" : {
            "default" : "block",
            "current" : "none",
            "options": {"block", "none"},
            "desc" : "Set to none to hide the DLC Available Content box."},
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
        if OS_TYPE == "Windows":
            subprocess.Popen(["explorer", path])
        elif OS_TYPE ==  "Darwin":
            subprocess.Popen(["open", path])
        elif OS_TYPE ==  "Linux":
            subprocess.Popen(["xdg-open", path])
        print("Opened: " + path)
    except:
        print_traceback()



def steam_dir():
    '''
    UTILITY: Returns Steam path for Windows, Mac, Linux.
    '''
    try:
        steam_path = ""
        if OS_TYPE == "Windows":
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "SOFTWARE\Valve\Steam")
            steam_path = winreg.QueryValueEx(key, "SteamPath")[0]
            steam_path = steam_path.replace("/","\\")
            #print(steamui_path)
        elif OS_TYPE ==  "Darwin":
            steam_path = os.path.expandvars('$HOME') + "/Library/Application Support/Steam"
        elif OS_TYPE ==  "Linux":
            steam_path = os.path.expandvars('$HOME') + "/.steam/steam"
        return steam_path
    except:
        print("Steam directory not found. Is Steam installed/has been run under this User?", file=sys.stderr)
        print_traceback()
        
def package_dir():
    '''
    UTILITY: Returns Steam package path (/package) for Windows, Mac, Linux.
    '''
    package_path = steam_dir() + "/package"
    if OS_TYPE == "Windows":
        package_path = package_path.replace("/","\\")
    return package_path
    
def library_dir():
    '''
    UTILITY: Returns Steam library path (/steamui) for Windows, Mac, Linux.
    '''
    library_path = steam_dir() + "/steamui"
    if OS_TYPE == "Windows":
        library_path = library_path.replace("/","\\")
    return library_path

def skins_dir():
    '''
    UTILITY: Returns Steam skins path (steamui/skins/OldGlory) for Windows, Mac, Linux.
    '''
    skins_path = library_dir() + "/skins/OldGlory"
    if OS_TYPE == "Windows":
        skins_path = skins_path.replace("/","\\")
    return skins_path

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
        
    
def get_git_file_hash(filepath, encoding="UTF-8"):
    '''
    UTILITY: Returns the git SHA hash of a file.
    '''
    try:
        #exclude .png for filehash
        if os.path.isfile(filepath) and os.path.splitext(filepath)[1] != ".png":
            with open(filepath, 'r', encoding=encoding) as f, \
                open(filepath + ".temp", 'w', encoding=encoding, newline='\n') as f1:
                f1.writelines(f.readlines())
            f.close()
            f1.close()

            filesize_bytes = os.path.getsize(filepath + ".temp")

            s = hashlib.sha1()
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

def get_md5_file_hash(filepath):
    '''
    UTILITY: Returns the MD5 hash of a file.
    '''
    try:
        #exclude .png for filehash
        if os.path.isfile(filepath):
            with open(filepath, "rb") as f:
                file_hash = hashlib.md5()
                while chunk := f.read(8192):
                    file_hash.update(chunk)
            return file_hash.hexdigest()
    except:
        print("Unable to get hash of file: " + filepath, file=sys.stderr)
        print_traceback()
        
def get_path_with_wildcard(filepath = r"C:\Program Files (x86)\Steam\package",
                           search_term = "steamui_websrc_all.zip.vz.*"):
    '''
    UTILITY: Returns the filepath (filename) of file using a search wildcard
        defaults to Steam\package steamui_websrc_all.zip.vz.* file
    '''
    #if os.path.isfile(Path(filepath).glob(search_term)):
    return next(Path(filepath).glob(search_term))

### Check CSS Patched
def is_css_patched(filename="2.css"):
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


CREATE_NO_WINDOW = 0x08000000

def process_exists(process_name):
    if OS_TYPE == "Windows":
        #check list of tasks (and hide console window)
        progs = str(subprocess.check_output('tasklist', creationflags=CREATE_NO_WINDOW))
        if process_name in progs:
            return True
        else:
            return False
    
    if OS_TYPE == "Linux":
        result = subprocess.run(['pgrep', '-f', process_name], stdout=subprocess.PIPE)
        output = result.stdout.decode().strip()
        
        if output:
            return True
        else:
            return False
    else:
        return False
    

def steam_exists():
    if OS_TYPE == "Windows":
        return process_exists("steam.exe")
    elif OS_TYPE ==  "Darwin":
        return False
    elif OS_TYPE ==  "Linux":
        return process_exists("steam")


### [END OF] GENERAL UTILITY Functions
##########################################


##########################################
### JSON Functions
def get_json_data(json_data_filename='old_glory_data.json'):
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

def write_json_data(json_data, json_data_filename='old_glory_data.json'):
    '''
    JSON: write JSON file using json_data object
    '''
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
    '''
    Load config file in TOML format and returns a Python dictionary object containing that config
    '''
    config_dict = {}
    if not os.path.isfile(config_filename) :
        print("Config file " + config_filename + " not found. Creating copy with default options.", file=sys.stderr)
        write_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG
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

def test_config():
    config = configparser.ConfigParser()
    config.optionxform = str
    config.read("oldglory_config2.cfg")
    return config

def write_config(config_dict = DEFAULT_CONFIG, filename = "oldglory_config2.cfg"):
    '''
    Takes a Python dictionary object and writes a config file in TOML format
    '''
    config = configparser.ConfigParser()
    config.optionxform = str
    for section in config_dict:
        config[section] = config_dict[section]
    #print(config.sections())
    #print(config.options("Main_Settings"))
    with open(filename, "w", newline='', encoding="UTF-8") as config_file:
        config.write(config_file)
    config_file.close()
    print("Updated config file. (" + filename + ")")

### [END OF] CONFIG Functions
##########################################


##########################################
### SETTINGS Functions
###   GUI Checkboxes
###   Need to change logic to cover "unchecking" options

def validate_settings(settings):
    '''
    UNIMPLEMENTED
    '''
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
    "HomeButton" : {"filename" : "module_homeicon"},
    "ThemeSelected" : ""
}

def read_css_sections(filename = "scss/libraryroot.custom.scss"):
    '''
    Read a list of SCSS imports and returns a Python dictionary containing each import as a "section"
    '''
    try:
        sections_data = {}
        with open("scss/libraryroot.custom.scss", "r", newline='', encoding="UTF-8") as f:
            import_prefix = '@import "./'
            import_suffix = '";'
            themes_prefix = '@import "../themes/'
            start_comment = '//'
            for line in f:
                if import_prefix in line:
                    if line.startswith(start_comment):
                        parsed_line = LineParser.remove_start_comment(start_comment, line)
                        parsed_line2 = LineParser.remove_import_prefix(import_prefix, parsed_line)
                        section = LineParser.remove_import_suffix(import_suffix, parsed_line2).rstrip(OS_line_ending())
                        sections_data[section] = "0"
                    else:
                        parsed_line = LineParser.remove_import_prefix(import_prefix, line)
                        section = LineParser.remove_import_suffix(import_suffix, parsed_line).rstrip(OS_line_ending())
                        sections_data[section] = "1"
        f.close()
        print("Loaded CSS Sections. " + "(" + filename + ")")
        return sections_data
    except:
        print("Error reading " + filename, file=sys.stderr)
        print_traceback()
    pass

def write_css_sections(sections, sections_filedata, sections_json,
                       filepath="scss/libraryroot.custom.scss",
                       temp_filepath="scss/libraryroot.custom.temp.scss"):
    '''
    takes two dictionaries of imports as "sections" compares them and writes to libraryroot.custom.scss
    sections            list of sections with values 0 or 1 depending on disabled/enabled
    
    sections_filedata   list of sections with values 0 or 1 from the original file, to compare
    
    sections_json       json data
    '''
    try:
        with open(filepath, "r", newline='', encoding="UTF-8") as f, \
             open(temp_filepath, "w", newline='', encoding="UTF-8") as f1:

            import_prefix = '@import "./'
            themes_prefix = '@import "../themes/'
            start_comment = '//'
            modify = 0
            for line in f:
                if import_prefix in line:
                    for section in sections:
                        #print(section)
                        if import_prefix + section in line:
                            if sections[section] == "1": 
                                if section in sections_filedata \
                                and sections[section] != sections_filedata[section]:
                                    #print("CHANGED SECTION "+ section)
                                    modify = 1
                                    f1.write(LineParser.remove_start_comment(start_comment, line))
                            elif sections[section] == "0":
                                if section in sections_filedata \
                                and sections[section] != sections_filedata[section]:
                                    #print("CHANGED SECTION "+ section)
                                    modify = 1
                                    f1.write(LineParser.add_start_comment(start_comment, line))
                            else:
                                print("Invalid value for section " + section, file=sys.stderr)
                    if modify == 0:
                        f1.write(line)
                    modify = 0
                else:
                    f1.write(line)                    
        f.close()
        f1.close()
        
        ###
        shutil.move(filepath, filepath + ".backup1")
        shutil.move(temp_filepath, filepath)
    except:
        print("Error enabling/disabling CSS sections,\nat " + line, file=sys.stderr)
        print_traceback()
    pass

       
def write_css_settings(settings,
                       filepath="scss/libraryroot.custom.scss",
                       temp_filepath="scss/libraryroot.custom.temp.scss"):
    '''
    Takes a dictionary of "settings" and writes to libraryroot.custom.scss
    '''
    try:
        with open(filepath, "r", newline='', encoding="UTF-8") as f, \
             open(temp_filepath, "w", newline='', encoding="UTF-8") as f1:

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
        shutil.move(filepath, filepath + ".backup1")
        shutil.move(temp_filepath, filepath)
            
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
    
    @staticmethod
    def remove_import_prefix(import_prefix, line):
        #strips import_prefix and any spaces before line
        return line.split(import_prefix)[1].lstrip()
    
    @staticmethod
    def add_import_prefix(import_prefix, line):
        #Concatenates import_prefix to line
        return import_prefix + line
    
    @staticmethod
    def remove_import_suffix(import_suffix, line):
        #strips import_suffix
        return line.split(import_suffix)[0]
    
    @staticmethod
    def add_import_suffix(import_suffix, line):
        #Concatenates import_suffix to line
        return line + import_suffix

def compile_css(json_data,
                filepath="libraryroot.custom.css",
                temp_filepath="libraryroot.custom.temp.css"):
    '''
    Compiles libraryroot.custom.css from /scss directory
    Adds variables.css
    '''
    try:
        sass.compile(dirname=('scss','.'),
                     output_style='expanded')
        with open(filepath, "r", newline='', encoding="UTF-8") as f, \
             open(temp_filepath, "w", newline='', encoding="UTF-8") as f1:
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
        print("CSS compiled.")
    except:
        print("Error compiling SCSS to CSS", file=sys.stderr)
        print_traceback()
        
    ###
    #shutil.move("libraryroot.custom.css", "libraryroot.custom.css.backup")
    shutil.move(temp_filepath, filepath)


### Triggers on Reload Config (button)
### From :root in css file -> CSS Config dict
def load_css_configurables(css_config_filename="variables.css"):
    '''
    Reads a .css file containing CSS variables and returns a Python dictionary'''
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
        

def write_css_configurables(css_config, css_config_filename = "variables.css"):
    '''
    Takes a Python dictionary and writes it to a .css file containing CSS variables
    '''
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
    '''
    Takes a Python dictionary and return an array of lines of CSS to be written
    '''
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
def enable_css_theme(theme_name, order, json_data):
    print("Enabling themes...")
    #print(theme_filename + order)
    #print(json_data)
    library_files = ["libraryroot.custom.css"]
    try:
        with open("scss/libraryroot.custom.scss", "r", newline='', encoding="UTF-8") as f, \
             open("scss/libraryroot.custom.temp.scss", "w", newline='', encoding="UTF-8") as f1:
            themereading = 0
            print(os.path.join("themes", theme_name, "libraryroot.custom.css"))
            for line in f:                
                if themereading == 1:
                    if line != OS_line_ending():
                        pass
                    for library_file in library_files:
                        if order == "before" and os.path.exists(os.path.join("themes", theme_name, library_file)):
                            #print("theme line")
                            f1.write('@import \"../themes/' + theme_name + "/" + library_file.rsplit(".",1)[0] + '\";' + OS_line_ending())
                        else:
                            f1.write(OS_line_ending())
                    themereading = 0
                elif themereading == 2:
                    if line != OS_line_ending():
                        pass
                    for library_file in library_files:
                        if order == "after" and os.path.exists(os.path.join("themes", theme_name, library_file)):
                            #print("theme line")
                            f1.write('@import \"../themes/' + theme_name + "/" + library_file.rsplit(".",1)[0] + '\";' + OS_line_ending())
                        else:
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
            if theme_name == "steam-library":
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
        print("Don't forget to run Apply config.css in Advanced Options if needed.")
        if not os.path.isfile("themes/config.css"):                             # if config.css in OldGlory themes/ doesn't exist
            shutil.copy2("themes/config.css.original", "themes/config.css")     # make a copy from config.css.original
            print("created themes/config.css from themes/config.css.original")
        if overwrite == 1:
            shutil.copy2("themes/config.css", library_dir() + "/" + "config.css")   # copy config.css from OldGlory themes/ to steamui/
            print("themes/config.css copied to: " + library_dir() + "/" + "config.css")
    except FileNotFoundError:
        print("config.css not found", file=sys.stderr)
        print_traceback()
    pass

def apply_friends_css():
    pass

### [END OF] APPLY CSS THEME Functions
##########################################

##########################################
### Patch CSS
def patch_css():
    try:
        patched_text = "/*patched*/\n"
        original_text = "/*original*/\n"
        css_dir = os.path.join(library_dir(), "css")
        for filename in os.listdir(css_dir):
            filepath = os.path.join(css_dir, filename)
            filesize = os.stat(filepath).st_size
            #print(filepath + " " + str(filesize))
            if os.path.isfile(filepath):
                with open(filepath, newline='', encoding="UTF-8") as f:
                    first_line = f.readline()
                    if patched_text[0:-1] in first_line:
                        print("File " + filename + " already patched.")
                    elif original_text[0:-1] in first_line:
                        pass
                    elif ".original" in filename:
                        pass
                    else:
                        contents = patched_text + "@import url(\"https://steamloopback.host/" + "css/" + get_original_filename(filename) + "\");\n@import url(\"https://steamloopback.host/" + get_custom_filename() + "\");\n";
                        #print(contents)
                        #print(os.stat(filepath).st_size)
                        #print(os.stat(filepath).st_size - len(contents))

                        with open(filepath, newline='', encoding="UTF-8") as f1, \
                            open(os.path.join(css_dir, get_original_filename(filename)), "w", newline='', encoding="UTF-8") as f2:
                            #f2.write(original_text)
                            for line in f1:
                                f2.write(line)
                        f2.close()
                        f1.close()                    
                        with open(filepath, "w", encoding="UTF-8") as f3:
                            #print(filesize)
                            contents += "\t" * (filesize - utf8len(contents) - 3)
                            #print(tabs)
                            f3.write(contents)
                        f3.close()
                        
                        print("Patched file " + filename)
                        
                f.close()
        print("----------")
    except Exception as e:
        print("Error patching file " + filename, file=sys.stderr)
        print_traceback()
           
def unpatch_css():
    try:
        css_dir = os.path.join(library_dir(), "css")
        for filename in os.listdir(css_dir):
            if (os.path.isfile(os.path.join(css_dir, filename)) and
                not os.path.isfile(os.path.join(
                    css_dir, filename.rsplit(".")[0] + ".original." + filename.split(".")[-1])
                                   )
                ):
                print("File " + filename + " already unpatched.")
            elif filename.endswith(".original.css"):
                orig_filename = filename.split(".")[0] + "." + filename.split(".")[2]
                #print(orig_filename)
                shutil.move(os.path.join(css_dir, filename), os.path.join(css_dir, orig_filename))
                print("Unpatched file " + orig_filename)
        print("----------")            
    except Exception as e:
        print("Error unpatching file " + filename, file=sys.stderr)
        print_traceback()
    
            
    
def utf8len(s):
    return len(s.encode('utf-8'))
                
def get_original_filename(filename):
    original_filename = filename.rsplit(".", 1)
    return original_filename[0] + ".original." + original_filename[1]
    
def get_custom_filename():
    return "libraryroot.custom.css"

##########################################
### JS Functions
### fixes.txt

### Load state of JS Fixes (enabled, disabled) from file fixes.txt
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
            sizes_dict = {}
            for line in infile:
                if re.match("### ===.*===", line):
                    readfix = 1
                    sectionhead = 1
                    fixname = line
                    fixname = re.sub("### ===|===", "", line).strip()
                elif line.strip(' ') == '\n':
                    readfix = 0
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
                    ### rewritten
                    if "Change Game Image Grid Sizes" in fixname: # and re.search("r = ([0-9]+)", line):
                        #line_segments = line.split("  ")
                        sizes = ["Small", "Medium", "Large"]
                        for size in sizes:
                            if "PortraitWidth" + size in line:
                                #print(line)
                                value = re.findall("([0-9]+)", line)[1]
                                sizes_dict[size] = value
                        #size_names = ["PortraitWidthSmall", "PortraitWidthMedium", "PortraitWidthLarge"]
                        #size_values = re.findall("r = ([0-9]+)", line_segments[1])
                        #for i, value in enumerate(size_values):
                        #    sizes_dict[sizes[i]] = value
                        special_fixesdata[fixname] = sizes_dict
                    ### END
                elif readfix == 0:
                    state = 0
                sectionhead = 0              
        infile.close()
        
        print("Loaded JS Tweaks. " + "(" + js_fixes_filename + ")")
    except ValueError:
        print("(" + js_fixes_filename + ") Problem in line format from line: " + line + \
              "Is the line missing a double space?", file=sys.stderr)
        print_traceback()
    except FileNotFoundError:
        print("JS Tweaks file, '" + js_fixes_filename + "' not found", file=sys.stderr)
    except Exception as e:
        print("Error loading JS Tweaks (" + js_fixes_filename + ") from line: " + line, file=sys.stderr)
        print_traceback()
    return fixesdata, special_fixesdata
    
    

def write_js_fixes(fixesdata, special_fixesdata):
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
                        f1.write(sectionhead_line + '\n')
                        writefix = 1
                        sectionhead = 1
                if line.strip(' ') == '\n':
                    writefix = 0
                    f1.write('\n')
                if writefix == 1 and sectionhead == 0:
                    ### special fixes data
                    if "Change Game Image Grid Sizes" in current_fixname:
                        sizes = ["Small", "Medium", "Large"]
                        for size in sizes:
                            if "PortraitWidth" + size in line:
                                newline = re.sub(r'^((.*?([0-9]+).*?){1})([0-9]+)',
                                r'\g<1>{}'.format(special_fixesdata[current_fixname][size]), line)
                                line = newline
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
                    
def backup_libraryroot_css(install_location="SFP/Millennium"):
    try:
        local_libraryroot_custom_css = "libraryroot.custom.css"
        if install_location == "steamui":
            libraryroot_dir = library_dir()
            libraryroot_custom_css = os.path.join(library_dir(), "libraryroot.custom.css")
            libraryroot_custom_css_backup = os.path.join(library_dir(),  "libraryroot.custom.css.backup")
            libraryroot_custom_css_backup2 = os.path.join(library_dir(), "libraryroot.custom.css.backup2")
        elif install_location == "SFP/Millennium":
            local_skin_json = "skin.json"
            skin_json = os.path.join(skins_dir(), "skin.json")
            skin_json_backup = os.path.join(skins_dir(), "skin.json.backup")
            libraryroot_dir = skins_dir()
            libraryroot_custom_css = os.path.join(skins_dir(), "libraryroot.custom.css")
            libraryroot_custom_css_backup = os.path.join(skins_dir(), "libraryroot.custom.css.backup")
            libraryroot_custom_css_backup2 = os.path.join(skins_dir(), "libraryroot.custom.css.backup2")
        elif install_location == "Local":
            libraryroot_custom_css = "libraryroot.custom.css"
            libraryroot_custom_css_backup = "libraryroot.custom.css.backup"
            libraryroot_custom_css_backup2 = "libraryroot.custom.css.backup2"
        else:
            raise Exception("Invalid install location/type", file=sys.stderr)
        
        if install_location == "SFP/Millennium" or install_location == "steamui":
            if os.path.isfile(libraryroot_custom_css):
                print("Existing libraryroot.custom.css code detected.")
                if os.path.isfile(libraryroot_custom_css_backup):
                    shutil.copy2(libraryroot_custom_css, libraryroot_custom_css_backup2)
                    print("Backed up libraryroot.custom.css to " + libraryroot_custom_css_backup2)
                else:
                    shutil.copy2(libraryroot_custom_css, libraryroot_custom_css_backup)
                    print("backed up libraryroot.custom.css to " + libraryroot_custom_css_backup)
                shutil.copy2(local_libraryroot_custom_css, libraryroot_custom_css)
            elif not os.path.isfile(libraryroot_custom_css):
                Path(libraryroot_dir).mkdir(parents=True, exist_ok=True)
                shutil.copy2(local_libraryroot_custom_css, libraryroot_custom_css)
            print("File " + local_libraryroot_custom_css + " written to " + libraryroot_custom_css)
            
        if install_location == "Local":
            if os.path.isfile(libraryroot_custom_css):
                print("Existing libraryroot.custom.css code detected.")
                if os.path.isfile(libraryroot_custom_css_backup):
                    shutil.copy2(libraryroot_custom_css, libraryroot_custom_css_backup2)
                    print("Backed up libraryroot.custom.css to " + libraryroot_custom_css_backup2)
                else:
                    shutil.copy2(libraryroot_custom_css, libraryroot_custom_css_backup)
                    print("backed up libraryroot.custom.css to " + libraryroot_custom_css_backup)
        
        if install_location == "SFP/Millennium":
            if os.path.isfile(skin_json):
                print("Existing skin.json code detected.")
                shutil.copy2(skin_json, skin_json_backup)
                print("backed up skin.json to skin.json.backup")
            shutil.copy2(local_skin_json, skin_json)
        
    except:
        print("Unable to copy libraryroot.custom.css to install location.", file=sys.stderr)
        print_traceback()

def clean_slate_css():
    '''
    Backs up and moves existing libraryroot.custom.css file
    '''
    try:
        #f = open(library_dir() + "/" + "libraryroot.empty.css", "w", newline='', encoding="UTF-8")
        #f.close()
        if os.path.isfile(os.path.join(library_dir(), "libraryroot.custom.css")):
            shutil.move(os.path.join(library_dir(), "libraryroot.custom.css"), os.path.join(library_dir(), "libraryroot.custom.css.backup"))
        #shutil.move(os.path.join(library_dir(), "libraryroot.empty.css"), os.path.join(library_dir(), "libraryroot.custom.css"))
        print("libraryroot.custom.css backed up at libraryroot.custom.css.backup")
        shutil.copy2("themes/config.css.original", os.path.join(library_dir(), "config.css"))
        
    except:
        print("Was not able to completely reset libraryroot.custom.css.", file=sys.stderr)
        print_traceback()

#rewrite so not hardcoded
def clear_js_working_files():
    try:
        json_data = get_json_data()
        files_to_remove = [json_data["libraryjsFile"], json_data["libraryjsBeautFile"], json_data["libraryjsOriginalFile"],
        json_data["libraryrootjsFile"], json_data["libraryrootjsBeautFile"], json_data["libraryrootjsOriginalFile"],
        json_data["jsFile"], json_data["jsBeautFile"], json_data["jsOriginalFile"]]
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
### STEAM Refresh functions

# Only works in Steam -dev mode
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
        
def request_url(url_address="http://localhost:8080/json/version"):
    with urllib.request.urlopen(url_address) as url:
        data = json.load(url)
        return data["webSocketDebuggerUrl"]

#Testing urllib3, not needed as performance is similar
def request_url_3(url_address="http://localhost:8080/json/version"):
    http = urllib3.PoolManager()
    response = http.request("GET", url_address)
    data = response.data
    values = json.loads(data)
    return values["webSocketDebuggerUrl"]
        
async def get_sharedjscontext(pages):
    for page in pages:
        title = await page.title()
        if title == "SharedJSContext":
            return page
        
async def connect_via_socket(socket_url):
    browser = await pyppeteer.connect(browserWSEndpoint=socket_url, defaultViewport=None)
    pages = await browser.pages()
    sharedjscontext = await get_sharedjscontext(pages)
    await sharedjscontext.reload()


async def refresh_steam(url):
    await connect_via_socket(url)


# requires Playwright and browser install
# not needed, see refresh_steam() 
def refresh_steam_playwright():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True, slow_mo=0)
        page = browser.new_page()
        page.goto("http://localhost:8080")
        page.get_by_text('SharedJSContext').click()
        page.wait_for_url(re.compile("http:\/\/localhost:8080\/devtools\/inspector.html\?ws=localhost:8080\/devtools\/page\/.*"))
        page.wait_for_timeout(300)
        page.keyboard.press('F5',delay=0)
        print("Steam window refreshed.")
        page.wait_for_timeout(300)
        browser.close()
        
### [END OF] STEAM Refresh Functions
##########################################


##########################################
### AUTO-UPDATE functions
BRANCH = "master"
        
def create_session():
    try:
        username = ''
        token = unscramble_token('2oyWzY_Uxy_KKmmEm5snDBnPnu2aZMZZU_lu99MRwFohNnWyosHTdHs8Uaf19SPsxypzJAs1HAplyvJMLFnmPTwqgjQML')
        session = requests.Session()
        session.auth = (username, token)
        return session
    except:
        print("Unable to request Github API session.", file=sys.stderr)
        print_traceback()

def unscramble_token(scrambled_token):
    charset = 'abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ_'
    keyset = 'xYjaXH2Woh7G6pkU9T4yz1qb8uDKcdZNilCVmLvBge5REMP0tA3rfswQSJIOnF_'
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
        #print(response.status_code) 
        return response.json()
    except json.decoder.JSONDecodeError as e:
        print("Error in update filelist JSON format.\nThis could be an issue with:\n" \
              "- " + list_filename + " on Github.\n" \
              "- Too many Github API requests (access token could have been removed)", file=sys.stderr)
        #print_traceback()
        print(e, file=sys.stderr)
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
    
def update_steamui_websrc_hash(json_data):
    json_data["steamui_websrc_all.zip.vz_hash"] = get_md5_file_hash(get_path_with_wildcard(package_dir()))
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
                        if os.path.exists(local_filepath) and os.path.isfile(local_filepath):
                            #if local hash != remote hash
                            if (get_git_file_hash(local_filepath) != filedata["sha"] and
                                 local_filepath != "scss/libraryroot.custom.scss" and
                                 local_filepath != "scss/_custom_module1.scss" and
                                 local_filepath != "scss/_custom_module2.scss"):                
                                #print("Different file hashes " + local_filepath)
                                #print(local_filepath + " | " + get_file_hash(local_filepath) + "  |  " + filedata["sha"])
                                print("New Version | " + local_filepath)
                                updatetype_files.append(local_filepath)
                            #print("", end="")
                        elif os.path.exists(local_filepath) and os.path.isdir(local_filepath):
                            print(local_filepath + " is directory")
                            dir_contents = get_repo_directory_contents(local_filepath)
                            #print(dir_contents)
                            for dir_filedata in dir_contents:
                                dir_filepath = local_filepath + "/" + dir_filedata["name"]
                                if (os.path.exists(dir_filepath) and
                                os.path.isfile(dir_filepath)):
                                    if (get_git_file_hash(dir_filepath) != filedata["sha"] and
                                    os.path.splitext(dir_filepath)[1] != ".png"):
                                        print("New Version | " + dir_filepath)
                                        updatetype_files.append(dir_filepath)
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
                open(filepath, 'w', encoding="UTF-8", newline='').write(r.text)
                print("File " + filepath + " downloaded.")
            else:
                print("Invalid request URL: " + filepath)
        else:
            print("File at " + filepath + " already exists!")
    except:
        print("Unable to download file " + str(filepath), file=sys.stderr)
        print_traceback()

### [END OF] AUTO-UPDATE Functions
##########################################