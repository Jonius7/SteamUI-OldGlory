#JS Tweaker for Steam Library UI by Jonius7
#libraries needed: jsbeautifier, jsmin

import jsbeautifier
import platform
import os
import sys
import shutil
import traceback
import re
from jsmin import jsmin
import time

LOCAL_DEBUG = 0 #Set to 1 to not copy files to/from Steam directory

# Determine Steam Library Path
OS_TYPE = platform.system()
if OS_TYPE == "Windows":
    import winreg

swap_js = {'"libraryroot"\}\[([a-z])=([a-z])\]\|\|([a-z])': '"libraryreet"}[\\1=\\2]||\\3'}
swapback_js = {'"libraryreet"\}\[([a-z])=([a-z])\]\|\|([a-z])': '"libraryroot"}[\\1=\\2]||\\3'}

fixes_dict = {}

def initialise():
    fixes_dict.clear() #not fixes_dict = {}

def library_dir():
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
        error_exit("Steam library directory could not be found.")


######


def copy_files_from_steam(reset=0): #set reset to 1 to overwrite files with fresh copy (useful for updates)
    try:
        if reset == 1 or LOCAL_DEBUG == 1:
            files_to_copy = ["library.js", "libraryroot.js"]
            for filename in files_to_copy:
                if not os.path.isfile(filename):
                    print("Copying file " + filename + " from Steam\steamui...")
                    shutil.copy2(library_dir() + "/" + filename, filename)
            if os.path.exists("libraryroot.beaut.js"):
                os.remove("libraryroot.beaut.js")
            
    except FileNotFoundError:
        error_exit("Steam directory and/or files not found.\n" \
              "Please check Steam\steamui for library.js and libraryroot.js")
            

def beautify_js():
    try:
        if not os.path.isfile("libraryroot.beaut.js"):
            print("Opening JS file and beautifying...")
            if not os.path.isfile("libraryroot.js"):
                shutil.copy2(library_dir() + "/libraryroot.js", "libraryroot.js")
            
            library = jsbeautifier.beautify_file("libraryroot.js")

            f = open("libraryroot.beaut.js", "wt", newline='', encoding="UTF-8")
            print("Writing beautified file... please do not close")
            f.write(library)
            f.close()
            print("Beautified file write finished")
    except:
        error_exit("libraryroot.js not found")

#modify library.js to look for different libraryroot.js file
def setup_library(reset=0):
    try:
        #if reset == 1 or LOCAL_DEBUG == 1:
        if not os.path.isfile("library.js"):
            shutil.copy2(library_dir() + "/library.js", "library.js")
        if reset == 0:
            print("library.js changing to use tweaked JS.")
            modify_library(swap_js)        
        elif reset == 1: #revert library.js to use original libraryroot.js file
            print("library.js reverting to use original JS.")
            modify_library(swapback_js)
    except:
        error_exit("Error setting up library.js")
        

def modify_library(swap_js_array):
    try:
        lines = []
        modified = 0
        with open('library.js', encoding="UTF-8") as infile:
            for line in infile:
                for src, target in swap_js_array.items():
                    new_line = re.sub(src, target, line)
                    #new_line = line.replace(src, target)
                    if new_line != line:
                        modified = 1
                lines.append(new_line)
        with open('library.js', 'w', encoding="UTF-8") as outfile:
            for line in lines:
                outfile.write(line)
        infile.close()
        outfile.close()
        if modified == 1:
            shutil.copy2("library.js", library_dir() + "/library.js")
            print("library.js copied over to " + library_dir() + "/library.js")
    except:
        error_exit("library.js not found")

def parse_fixes_file(filename):
    '''
    look through fixes file and add fixes to fixes_dict
    '''
    print("Finding Fixes...\n")
    global fixes_dict
    fixes_dict = {}
    try:
        with open(filename, newline='', encoding="UTF-8") as fi:
            lines = filter(None, (line.rstrip() for line in fi))
            try:
                for line in lines:
                    if not line.startswith('###'):
                        (key, val) = line.rstrip().split("  ")
                        if "~~" in key:
                            t = key.split("~~")
                            if len(t) == 2:
                                fixes_dict[t[1]] = {"prev" : t[0],
                                                    "replace" : val}
                            else:
                                error_exit("Unexpected number of ~~ in line: " + line)
                        #elif re.search(r"\d\$", key):
                        #    print("V")
                        #    print(key)
                        else:
                            fixes_dict[key] = {"replace" : val}
            except Exception as e:
                print("Error in line: " + line, file=sys.stderr)
                print(e, file=sys.stderr)
                fi.close()                
                error_exit("Invalid file format")
        fi.close()
    except FileNotFoundError:
        error_exit("fixes.txt not found")
    except Exception as e:
        error_exit("Error found while parsing fixes file: " + e)

def find_fix(line, fix):
    m_line = line.replace(fix, fixes_dict[fix]["replace"])
    #print("FIX: ", end = '')
    #print(m_line.strip())
    #print(fixes_dict[fix]["replace"])
    print("FIX: " + m_line.strip())
    return m_line

def find_fix_with_variable(line, fix):
    #res = [i.start() for i in re.finditer("\$\^", st)]
    #for lv in res:
    print("todo")
        

def write_modif_file():
    try:
        with open("libraryroot.beaut.js", "r", newline='', encoding="UTF-8") as f, \
             open("libraryroot.modif.js", "w", newline='', encoding="UTF-8") as f1:
            prev_line = ""
            for line in f:
                modified = 0
                for fix in fixes_dict:
                    if "prev" in fixes_dict[fix]:
                        if fixes_dict[fix]["prev"] in prev_line and fix in line:
                            f1.write(find_fix(line, fix))
                            modified = 1
                    elif fix in line:
                        f1.write(find_fix(line, fix))
                        modified = 1
                if modified == 0:
                    f1.write(line)
                prev_line = line
        f.close()
        f1.close()
    except:
        error_exit("Error writing libraryroot.modif.js")

def re_minify_file():
    try:
        print("\nRe-minify JS file")
        with open("libraryroot.modif.js", "r", newline='', encoding="UTF-8") as js_file:
            minified = jsmin(js_file.read())
        with open("libraryreet.js", "w", newline='', encoding="UTF-8") as js_min_file:
            js_min_file.write(minified)
        js_file.close()
        js_min_file.close()
        print("\nJS Minify complete.")
    except:
        error_exit("Error completing JS minify.")
    
def copy_files_to_steam():
    try:
        if LOCAL_DEBUG == 0:
            files_to_copy = ["libraryreet.js"]
            for filename in files_to_copy:
                shutil.copy2(filename, library_dir() + "/" + filename)
                print("File " + filename + " written to " + library_dir())
                
    except FileNotFoundError:
        error_exit("Files not found!\n" \
              "Run the other functions in js_tweaker first.")
    except Exception as e:
        error_exit("Error found while copying files to Steam: " + e)


def error_exit(errormsg):
    print(errormsg, file=sys.stderr)
    print("~~~~~~~~~~")
    print(traceback.print_exc(), file=sys.stderr)
    print("~~~~~~~~~~")
    sys.exit()
    
def main():
    print("JS Tweaker for Steam Library UI by Jonius7\n")
    initialise()
    copy_files_from_steam()
    beautify_js()
    setup_library()
    parse_fixes_file("fixes.txt")
    write_modif_file()
    re_minify_file()
    copy_files_to_steam()
    print("\nSteam Library JS Tweaks applied successfully.")
    time.sleep(2)
                
if __name__ == "__main__":
    main()
