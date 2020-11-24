import platform
import os
import sys
import shutil
import traceback
import re

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
            "desc" : "Leave at 0px, this var is for steam-library compatibility and vertical nav bar"}
        }
    }

SETTING_MAP = {"SteamLibraryPath" : "",
                  "PatcherPath" : "",
                  "" : "",
                  "InstallCSSTweaks" : "",
                  "EnablePlayButtonBox" : {"start" : "/* PLAY BAR LAYOUT - BETA */", "end" : "/* END PLAY BAR LAYOUT */"},
                  "EnableVerticalNavBar" : {"start" : "/* VERTICAL NAV BAR - BETA - REQUIRES JS TWEAKS */", "end" : "/* END VERTICAL NAV BAR */"},
                  "EnableClassicLayout" : {"start" : "/* CLASSIC LAYOUT - BETA */", "end" : "/* END CLASSIC LAYOUT */"},
                  "LandscapeImages" : {"start" : "/*HORIZONTAL GAME IMAGE TWEAKS*/", "end" : "/*END HORIZONTAL GAME IMAGE TWEAKS*/"},                
                  "InstallWithDarkLibrary" : ""
            }

ROOT_MAP = {"start" : ["Configurable variables", ":root {"],
            "end" : ["}", "======"]
            }

PATCHED_TEXT = "/*patched*/"

def OS_line_ending():
    if OS_TYPE == "Windows":
        return "\r\n"
    elif OS_TYPE ==  "Darwin":
        return "\n"
    elif OS_TYPE ==  "Linux":
        return "\n"
    
def library_dir():
    steamui_path = ""
    if OS_TYPE == "Windows":
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "SOFTWARE\Valve\Steam")
        steam_path = winreg.QueryValueEx(key, "SteamPath")[0]
        steamui_path = steam_path.replace("/","\\") + "\steamui"
        #print(steamui_path)
    elif OS_TYPE ==  "Darwin":
        steamui_path = os.path.expandvars('$HOME') + "/Library/Application Support/Steam" + "\steamui"
    elif OS_TYPE ==  "Linux":
        steamui_path = os.path.expandvars('$HOME') + "/.steam/steam" + "\steamui"
    return steamui_path

#Working Directory
#if not os.path.exists('config'):
#    os.makedirs('config')
'''
try:
    directory = "\config"
    os.chdir(os.getcwd() + directory)
except FileNotFoundError:
    print("Directory " + directory + " not found", file=sys.stderr)
'''



### Check CSS Patched
def is_css_patched():
    patched = False
    try:
        with open(library_dir() + "\\css\\libraryroot.css", newline='', encoding="UTF-8") as f:
            first_line = f.readline()
        if PATCHED_TEXT not in first_line:
            print("css\libraryroot.css not patched. Download SteamFriendsPatcher from\n" \
                  "https://github.com/PhantomGamers/SteamFriendsPatcher/releases", file=sys.stderr)
        else:
            patched = True
        f.close()
    except:
        print("css\libraryroot.css not found", file=sys.stderr)
    return patched


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
                        (key, val) = line.rstrip().replace(" ", "").split("=")
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
            print("DARK STEAM")
            validated_settings.extend(["InstallWithDarkLibrary"])
    #print(validated_settings)
    return validated_settings

### END
###


###
### CSS functions (libraryroot.custom.css)
###

def write_css_settings(settings, settings_values, root_config):
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
                    #print("YAHOO " + line)
                    startreading = 1
                    for line in css_root_writer(root_config):
                        f1.write(line + OS_line_ending())
                    
                elif ROOT_MAP["end"][0] in prevline and ROOT_MAP["end"][1] in line:
                    #print("PARTYEND")
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
                                    #print(setting + " CSS Start commented out")
                                    #print("Current Line | " + line)
                                    if settings_values[setting] == 1 and setting in settings:
                                        modify = 1
                                        f1.write(start_string + OS_line_ending())
                                else:
                                    if settings_values[setting] == 0:
                                        modify = 1
                                        f1.write(start_string + "/*" + OS_line_ending())
                                        #print(setting + " CSS Start not commented out (enabled)")
                            if end_string in line:
                                if "*/" + end_string in line:
                                    #print(setting + " CSS End commented out")
                                    #print("Current Line | " + line)
                                    if settings_values[setting] == 1 and setting in settings:
                                        modify = 1
                                        f1.write(end_string + OS_line_ending())
                                else:
                                    if settings_values[setting] == 0:
                                        modify = 1
                                        f1.write("*/" + end_string + OS_line_ending())
                                        #print(setting + " CSS End not commented out (enabled)")
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


### Triggers on Reload Config (button)
### From :root in css file -> CSS Config dict
def load_css_configurables():

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
        print("Error loading CSS configurables from line: " + line, file=sys.stderr)
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
            comment = value[1].lstrip()
            default = ""
            if "/* Default: " in comment:
                comment_m = comment.split("/* Default: ")[1].split(".", 1)
                #print(comment_m)
                default = comment_m[0].lstrip()
                #print(comment_m[1].strip()[:-2])
                desc = comment_m[1].split("*/")[0].strip()
            else:
                default = value[0]
                #print(comment)
                desc = comment.split("/*")[1].split("*/")[0].strip()
                
            #print(name[0] + "  |  " + default + "  |  " + value[0] + "  |  " + desc)
            return {"name" : name[0], "default" : default, "current" : value[0], "desc" : desc}
    except Exception as e:
        print("Some error in line: " + line, file=sys.stderr)
        print("~~~~~~~~~~")
        print(traceback.print_exc(), file=sys.stderr)
        print("~~~~~~~~~~")
        

#root writer
#from CSS_CONFIG dictionary to an array of lines of CSS to be written
def css_root_writer(css_config):
    #print("START ROOT WRITER")
    indent = "  "
    css_lines = []
    css_lines.append(":root {")
    for key in css_config:
        #print(key)
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

'''
def css_root_writer_example():
    indent = "  "
    file = open("rootfile.css", "w", newline='', encoding="UTF-8")
    for line in css_root_writer(CSS_CONFIG):
        file.write(line + OS_line_ending())
    file.close()
'''
### END
###



###
### APPLY CSS THEME Functions
###

BEFORE_THEME = {"shiina.css" :
                {"start" : "DO NOT EDIT THESE !!! DO NOT EDIT THESE",
                  "end" : "END steam-library tweaks for SteamUI-OldGlory"}
                }


### Order: CSS before or after SteamUI-OldGlory's CSS
def apply_css_theme(theme_filename, order, patchtext):
    print("TODO apply Theme")
    #print(filename)
    #print(order)
    #print(patchtext)
    #print("LINE2")
    theme_change_needed = remove_current_css_themes(theme_filename)
    if theme_change_needed:
        add_new_css_theme(theme_filename, order, patchtext)


def remove_current_css_themes(theme_filename):
    try:
        ### This is specifically for steam-library(shiina) or any theme that adds CSS "before"
        ### Would want a rewrite with some better conditional code
        with open("libraryroot.custom.css", "r", newline='', encoding="UTF-8") as f, \
             open("libraryroot.custom.theme.css", "w", newline='', encoding="UTF-8") as f1:
            to_remove = 0
            last_line = 0
            no_change = False #If False, theme will be added in add_new_css_theme.
            for line in f:
                if last_line == 1 and line.strip(' ') != OS_line_ending():
                    to_remove = 0
                    last_line = 0
                
                for theme in BEFORE_THEME:
                    if theme_filename not in theme: 
                        if BEFORE_THEME[theme]["start"] in line:
                            #print("ROUND 1")
                            to_remove = 1
                            print("Removing existing themes in libraryroot.custom.css...")
                        elif BEFORE_THEME[theme]["end"] in line:
                            last_line = 1
                            #print("ROUND 2")                        
                    elif theme_filename in theme: #if theme to apply is already in file, skip removing
                        no_change = True
                    
                if to_remove == 0:
                    f1.write(line)
        f.close()
        f1.close()

        ###
        shutil.move("libraryroot.custom.css", "libraryroot.custom.css.backup")
        shutil.move("libraryroot.custom.theme.css", "libraryroot.custom.css")

        return no_change

            
    except:
        print("libraryroot.css not found", file=sys.stderr)
        
def add_new_css_theme(theme_filename, order, patchtext):
    try:
        if order == "before":
            print("BEFORE")
            with open("libraryroot.custom.css", "r", newline='', encoding="UTF-8") as f, \
                 open("themes\\" + theme_filename, "r", newline='', encoding="UTF-8") as ft, \
                 open("libraryroot.custom.theme.css", "w", newline='', encoding="UTF-8") as f1:
                for line in ft:
                    f1.write(line)
                f1.write(OS_line_ending())
                for line in f:
                    f1.write(line)
            f.close()
            ft.close()
            f1.close()
            
            ###
            shutil.move("libraryroot.custom.css", "libraryroot.custom.css.backup")
            shutil.move("libraryroot.custom.theme.css", "libraryroot.custom.css")

            ###
            if theme_filename == "shiina.css":
                steam_library_compat_config()
            
            
        elif order == "after":
            patch_html(theme_filename)
            copy_theme_css_file(theme_filename)

            
    except:
        print("Error applying theme from " + theme_filename, file=sys.stderr)
        print("~~~~~~~~~~")
        print(traceback.print_exc(), file=sys.stderr)
        print("~~~~~~~~~~")


def patch_html(theme_filename):
    print("TODO patchhtml")
    try:
        if len(theme_filename) > 16:
            raise Exception('Filename too long. Please keep it to 16 characters or less.')
        with open(library_dir() + "\\index.html", "r", newline='', encoding="UTF-8") as f, \
             open("index.theme.html", "w", newline='', encoding="UTF-8") as f1:
            first_line = f.readline()
            second_line = f.readline()
            if first_line == "<!doctype html>" + OS_line_ending() and \
               second_line == "<html style=\"width: 100%; height: 100%\">" + OS_line_ending():
                print("Original HTML file detected.")
                shutil.copy2(library_dir() + "\\" + "index.html", "index.html.original")
                ### return to start
                f.seek(0)
                theme_html_length = 0
                for line in f:
                    #Strip spacing from : and ;
                    stripped_line = strip_spacing(line)
                    #print(stripped_line)
                    if stripped_line.strip() == '<script src="library.js"></script>':
                        theme_line = stripped_line.strip() + href_rel_stylesheet(theme_filename)
                        f1.write(theme_line)
                        theme_html_length += len(theme_line)
                    else:
                        f1.write(stripped_line.strip())
                        theme_html_length += len(stripped_line.strip())
                #check file sizes    
                #print(os.stat(library_dir() + "\\index.html").st_size)
                #print(theme_html_length)

                #Add filler
                filler = filler_text(os.stat(library_dir() + "\\index.html").st_size,
                                          theme_html_length)
                f1.write(filler)
                
            else:
                print("Patched HTML file detected.")
                print(os.stat(library_dir() + "\\index.html").st_size)
                
                old_href = '<script src=\"library.js\"></script><link href=\"themes/.*\" rel="stylesheet\">'  
                new_href = '<script src=\"library.js\"></script><link href=\"themes/' + theme_filename + '\" rel=\"stylesheet\">'
                
                ### return to start
                f.seek(0)               
                for line in f:
                    match = re.search(old_href, line)
                    #print(match)
                    if match:
                        theme_line = re.sub(old_href, new_href, line)
                        print(theme_line)
                        length_diff = len(new_href) - len(old_href)
                        print("DIFF")
                        print(length_diff)
                        if length_diff <= 0:
                            theme_line += filler_text(old_href, new_href)
                        elif length_diff > 0:
                            if length_diff > len(theme_line) - len(theme_line.rstrip()):
                                raise Exception('Unable to trim enough characters! Is filename too long?')
                            else:
                                theme_line = theme_line[0:-length_diff]
                        f1.write(theme_line)
                        
                        #print(len(theme_line))
                        #print(len(theme_line.rstrip()))
                    else:
                        f1.write(line)
  
        f.close()
        f1.close()

        print("Patching HTML File successful.")
    except FileNotFoundError:
        print("index.html.original not found, and could not be created.", file=sys.stderr)
    except Exception as e:
        print("Error configuring index.html", file=sys.stderr)
        print(e, file=sys.stderr)
        print("~~~~~~~~~~")
        print(traceback.print_exc(), file=sys.stderr)
        print("~~~~~~~~~~")


    ### String Helper functions
        
def strip_spacing(line):
    c_line = line.replace(": ", ":").replace("; ", ";")
    return c_line

def filler_text(original_length, new_length):
    length = original_length - new_length
    if length >= 0:
        filler_text = "\t" * length
        return filler_text
    else:
        raise Exception("Something is wrong with the length of the file. It's too long!\n" \
                        "Changes won't be applied (hopefully).")

def href_rel_stylesheet(href):
    return '<link href=\"themes/' + href + '\" rel=\"stylesheet\">'

    #########


def copy_theme_css_file():
    print("TODO copy to themes/themecss")

def steam_library_compat_config():
    print("TODO find and replace config.css")

### END 
### 



###
### JS functions (fixes.txt)
### Load state of JS Fixes (enabled, disabled) from file
def load_js_fixes():
    try:
        fixesdata = {}
        special_fixesdata = {}
        fixname = ""
        readfix = 0
        sectionhead = 0
        state = 3 #0 = disabled(commented out), 1 = enabled, 2 = mixed, starting

        with open('fixes.txt', newline='', encoding="UTF-8") as infile:
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
                        #print(special_fixesdata)
                        #print("!~!$!@$~!$!")
                        #print(re.sub("n = ([0-9]+)", "n = AAA", line_segments[1]))
                        #print("~~~~~~~~")
                        #print("  ".join(line_segments))
        
                elif readfix == 0:
                    state = 0
                sectionhead = 0               
        infile.close()
        
        print("Loaded JS Tweaks.")
    except ValueError:
        print("(fixes.txt) Problem in line format from line: " + line + \
              "Is the line missing a double space?", file=sys.stderr)
    except FileNotFoundError:
        print("JS Tweaks file, 'fixes.txt' not found", file=sys.stderr)
    except Exception as e:
        print("Error loading JS Tweaks (fixes.txt) from line: " + line, file=sys.stderr)
        print("~~~~~~~~~~")
        print(traceback.print_exc(), file=sys.stderr)
        print("~~~~~~~~~~")
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
        print("~~~~~~~~~~")
        print(traceback.print_exc(), file=sys.stderr)
        print("~~~~~~~~~~")
                    
def refresh_steam_dir():
    shutil.copy2("libraryroot.custom.css", library_dir() + "\\" + "libraryroot.custom.css")
    print("File " + "libraryroot.custom.css" + " written to " + library_dir())
    shutil.copy2(library_dir() + "\\licenses.txt", library_dir() + "\\licenses.txt.copy")
    os.remove(library_dir() + "\\licenses.txt.copy")
