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
######

def copy_files_from_steam(reset=0): #set reset to 1 to overwrite files with fresh copy (useful for updates)
    try:
        if reset == 1 or LOCAL_DEBUG == 1:
            files_to_copy = ["library.js", "libraryroot.js"]
            for filename in files_to_copy:
                if not os.path.isfile(filename):
                    print("Copying files from Steam\steamui...")
                    shutil.copy2(library_dir() + "/" + filename, filename)
            os.remove("libraryroot.beaut.js")
    except FileNotFoundError:
        print("Steam directory and/or files not found.\n" \
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
    #if reset == 1 or LOCAL_DEBUG == 1:
    if not os.path.isfile("library.js"):
        shutil.copy2(library_dir() + "/library.js", "library.js")
    if reset == 0:
        modify_library(swap_js)
        print("library.js changed to use tweaked JS.")
    elif reset == 1: #revert library.js to use original libraryroot.js file
        modify_library(swapback_js)
        print("library.js reverted to use original JS.")
    


def modify_library(swap_js_array):
    try:
        lines = []
        modified = 0
        with open('library.js') as infile:
            for line in infile:
                for src, target in swap_js_array.items():
                    new_line = re.sub(src, target, line)
                    #new_line = line.replace(src, target)
                    if new_line != line:
                        modified = 1
                lines.append(new_line)
        with open('library.js', 'w') as outfile:
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
    print("Finding Fixes...\n")
    try:
        with open("fixes.txt", newline='', encoding="UTF-8") as fi:
            lines = filter(None, (line.rstrip() for line in fi))
            try:
                for line in lines:
                    if not line.startswith('###'):
                        (key, val) = line.rstrip().split("  ")
                        fixes_dict[key] = val
            except Exception as e:
                print("Error in line" + line, file=sys.stderr)
                print(e, file=sys.stderr)
                fi.close()                
                error_exit("Invalid file format")
        fi.close()
    except FileNotFoundError:
        error_exit("fixes.txt not found")
    except Exception as e:
        error_exit("Unknown error: " + e)

def find_fix(line, fix):
    m_line = line.replace(fix, fixes_dict[fix])
    #print("FIX: ", end = '')
    #print(m_line.strip())
    print("FIX: " + m_line.strip())
    return m_line

def write_modif_file():
    with open("libraryroot.beaut.js", "r", newline='', encoding="UTF-8") as f, \
         open("libraryroot.modif.js", "w", newline='', encoding="UTF-8") as f1:
        for line in f:
            modified = 0
            for fix in fixes_dict:
                if fix in line:
                    f1.write(find_fix(line, fix))
                    modified = 1
            if modified == 0:
                f1.write(line)
    f.close()
    f1.close()

def re_minify_file():
    print("\nRe-minify JS file")
    with open("libraryroot.modif.js", "r", newline='', encoding="UTF-8") as js_file:
        minified = jsmin(js_file.read())
    with open("libraryreet.js", "w", newline='', encoding="UTF-8") as js_min_file:
        js_min_file.write(minified)
    js_file.close()
    js_min_file.close()
    
def copy_files_to_steam():
    try:
        if LOCAL_DEBUG == 0:
            files_to_copy = ["libraryreet.js", "fixes.txt"]
            for filename in files_to_copy:
                shutil.copy2(filename, library_dir() + "/" + filename)
                print("File " + filename + " written to " + library_dir())
                
    except FileNotFoundError:
        print("Files not found!\n" \
              "Run the other functions in js_tweaker first.")


def error_exit(errormsg):
    print(errormsg, file=sys.stderr)
    print("~~~~~~~~~~")
    print(traceback.print_exc(), file=sys.stderr)
    print("~~~~~~~~~~")
    input("Press Enter to continue...")
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
