#JS Tweaker for Steam Library UI by Jonius7
#libraries needed: jsbeautifier, jsmin

import jsbeautifier
import platform
import os
import sys
import shutil
import traceback
import re
import rjsmin
import time

LOCAL_DEBUG = 0 #Set to 1 to not copy files to/from Steam directory

# Determine Steam Library Path
OS_TYPE = platform.system()
if OS_TYPE == "Windows":
    import winreg

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

files_to_copy = ["library.js", "libraryroot.js","3991.js"]

def copy_files_from_steam(reset=0): #set reset to 1 to overwrite files with fresh copy (useful for updates)
    try:
        if reset == 1 or LOCAL_DEBUG == 1:
            for filename in files_to_copy:
                if os.path.exists(library_dir() + "/" + filename):
                    print("Copying file " + filename + " from Steam\steamui...")
                    shutil.copy2(library_dir() + "/" + filename, filename)
            
    except FileNotFoundError:
        error_exit("Steam directory and/or files not found.\n" \
              "Please check Steam\steamui for library.js and libraryroot.js")

def backup_files_from_steam():
     for filename in files_to_copy:
        #if os.path.exists(library_dir() + "/" + filename):
        #    shutil.copy2(library_dir() + "/" + filename, library_dir() + "/" + filename + ".original")
        if not os.path.exists(filename + ".original"):
            shutil.copy2(library_dir() + "/" + filename, filename + ".original")
            
def get_beaut_filename(filename):
    beaut_filename = filename.rsplit(".", 1)
    return beaut_filename[0] + ".beaut." + beaut_filename[1]

def get_modif_filename(filename):
    modif_filename = filename.rsplit(".", 1)
    return modif_filename[0] + ".modif." + modif_filename[1]

def beautify_js(filename="libraryroot.js"):
    try:
        beautify_file = get_beaut_filename(filename)
        if not os.path.isfile(beautify_file):
            print("Opening " + beautify_file + ", generating beautified JS...")
            if not os.path.isfile(filename):
                shutil.copy2(os.path.join(library_dir(), filename), filename)

            opts = jsbeautifier.default_options()
            #opts.eol = ""
            library = jsbeautifier.beautify_file(filename, opts)

            f = open(beautify_file, "wt", newline='', encoding="UTF-8")
            f.write(library)
            f.close()
            print("Beautified file write finished")
    except:
        error_exit("libraryroot.js not found")

#modify library.js to look for different libraryroot.js file
'''def setup_library(reset=0):
    try:
        #if reset == 1 or LOCAL_DEBUG == 1:
        if not os.path.isfile("library.js"):
            shutil.copy2(library_dir() + "/library.js", "library.js")
        if reset == 0:
            print("library.js changing to use tweaked JS. (librery.js)")
            modify_library(swap_js)        
        elif reset == 1: #revert library.js to use original libraryroot.js file
            print("library.js reverting to use original JS.")
            reset_html()
    except:
        error_exit("Error setting up library.js")'''
        
'''def modify_library(swap_js_array):
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
        infile.close()
        if modified == 1:
            with open('librery.js', 'w', encoding="UTF-8") as outfile:
                for line in lines:
                    outfile.write(line)
            
            outfile.close()        
            shutil.copy2("librery.js", library_dir() + "/librery.js")
            print("librery.js copied over to " + library_dir() + "/librery.js")
    except:
        error_exit("library.js not found")'''

def modify_html():
    html_array = {"/library.js": "/librery.js"}
    
    try:
        lines = []
        modified = 0
        with open(library_dir() + "/index.html", encoding="UTF-8") as infile:
            for line in infile:
                for src, target in html_array.items():
                    new_line = re.sub(src, target, line)
                    if new_line != line:
                        modified = 1
                lines.append(new_line)
        infile.close()
        if modified == 1:
            with open(library_dir() + "/index.html.temp", 'w', encoding="UTF-8") as outfile:
                for line in lines:
                    outfile.write(line)            
            outfile.close()
            
            shutil.move(library_dir() +"/index.html", library_dir() + "/index.html.original")
            shutil.move(library_dir() +"/index.html.temp", library_dir() + "/index.html")
            print("index.html changing to use tweaked JS.")
            print("index.html backup created at " + library_dir() + "/index.html.original")
    except:
        error_exit("index.html unable to be patched.")

def reset_html():
    try:
        if os.path.isfile(library_dir() + "/index.html.original"):
            shutil.move(library_dir() + "/index.html.original", library_dir() + "/index.html")
            print(library_dir() + "/index.html replaced with backup: " + "index.html.original")
    except:
        error_exit("Unable to reset index.html")
            

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

def find_fix(line, fix, filename):
    m_line = line.replace(fix, fixes_dict[fix]["replace"])
    #print("FIX: ", end = '')
    #print(m_line.strip())
    #print(fixes_dict[fix]["replace"])
    print("FIX (" + filename + "): " + m_line.strip())
    return m_line

def find_fix_with_variable(line, fix):
    #res = [i.start() for i in re.finditer("\$\^", st)]
    #for lv in res:
    print("todo")
        

def write_modif_file(filename = "libraryroot.js"):
    beaut_filename = get_beaut_filename(filename)
    modif_filename = get_modif_filename(filename)
    try:
        
        with open(beaut_filename, "r", newline='', encoding="UTF-8") as f, \
             open(modif_filename, "w", newline='', encoding="UTF-8") as f1:
            prev_line = ""
            for line in f:
                modified = 0
                for fix in fixes_dict:
                    if "prev" in fixes_dict[fix]:
                        if fixes_dict[fix]["prev"] in prev_line and fix in line:
                            f1.write(find_fix(line, fix, filename))
                            modified = 1
                    elif fix in line:
                        f1.write(find_fix(line, fix, filename))
                        modified = 1
                if modified == 0:
                    f1.write(line)
                prev_line = line
        f.close()
        f1.close()
    except:
        error_exit("Error writing " + modif_filename)

def re_minify_file(modif_filename = "libraryroot.modif.js", min_filename = "libraryreet.js"):
    try:
        print("\nRe-minify JS file")
        with open(modif_filename, "r", newline='', encoding="UTF-8") as js_file:
            minified = rjsmin.jsmin(js_file.read(), keep_bang_comments=True)
        with open(min_filename, "w", newline='', encoding="UTF-8") as js_min_file:
            js_min_file.write(minified)
        js_file.close()
        js_min_file.close()
        print("JS Minify complete. (" + min_filename + ")")
    except:
        error_exit("Error completing JS minify.")

def compress_newlines(filename = "librery.js"):
    with open(filename, encoding="UTF-8") as f1, \
        open(filename + ".compress", "w", newline='', encoding="UTF-8") as f2:
        output = " ".join(f1.read().splitlines())
        f2.write(output)
    f1.close()
    f2.close()

    os.remove(filename)
    shutil.move(filename + ".compress", filename)       

#hardcoded values
def copy_files_to_steam():
    try:
        if LOCAL_DEBUG == 0:
            files_to_copy = {"librery.js": "library.js",
                             "libraryreet.js": "libraryroot.js",
                             "3992.js": "3991.js"}
            for filename in files_to_copy:
                shutil.copy2(filename, library_dir() + "/" + files_to_copy[filename])
                print("File " + filename + " written to " + library_dir() + "/" + files_to_copy[filename])
                
    except FileNotFoundError:
        error_exit("Files not found!: " + filename + "\n" \
              "Do you need to configure other files first?")
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
    '''initialise()
    copy_files_from_steam()
    setup_library()
    modify_html()
    beautify_js()
    beautify_js("library.js")    
    parse_fixes_file("fixes.txt")
    write_modif_file()
    write_modif_file("library.js")
    re_minify_file()
    re_minify_file("library.modif.js", "librery.js")
    compress_newlines("librery.js")
    copy_files_to_steam()
    print("\nSteam Library JS Tweaks applied successfully.")
    time.sleep(2)'''
                
if __name__ == "__main__":
    main()
