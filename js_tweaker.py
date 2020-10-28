#JS Tweaker for Steam Library UI by Jonius7
#libraries needed: jsbeautifier, jsmin


import jsbeautifier
import os.path
import sys
from jsmin import jsmin
import time

   
swap_js = {'"libraryroot"}[n=u]||n': '"libraryreet"}[n=u]||n'}
swapback_js = {'"libraryreet"}[n=u]||n': '"libraryroot"}[n=u]||n'}

fixes_dict = {}

def beautify_js():
    if not os.path.isfile("libraryroot.beaut.js"):
        print("Opening JS file and beautifying...")
        library = jsbeautifier.beautify_file("libraryroot.js")

        f = open("libraryroot.beaut.js", "wt", newline='', encoding="UTF-8")
        print("Writing beautified file... please do not close")
        f.write(library)
        f.close()
        print("Beautified file write finished")


#modify library.js to look for different libraryroot.js file
def setup_library():
    modify_library(swap_js)

#revert library.js to use original libraryroot.js file
def revert_library():
    modify_library(swapback_js)
    
def modify_library(swap_js_array):
    try:
        lines = []
        with open('library.js') as infile:
            for line in infile:
                for src, target in swap_js_array.items():
                    line = line.replace(src, target)
                lines.append(line)
        with open('library.js', 'w') as outfile:
            for line in lines:
                outfile.write(line)
        infile.close()
        outfile.close()
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
    print("FIX: ", end = '')
    print(m_line.strip())
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
    with open("libraryroot.modif.js", "r", newline='', encoding="UTF-8") as js_file:
        minified = jsmin(js_file.read())
    with open("libraryreet.js", "w", newline='', encoding="UTF-8") as js_min_file:
        js_min_file.write(minified)
    js_file.close()
    js_min_file.close()
    print("\nRe-minify JS file")

def error_exit(errormsg):
    print(errormsg, file=sys.stderr)
    input("Press Enter to continue...")
    sys.exit()
    
def main():
    beautify_js()
    setup_library()
    parse_fixes_file("fixes.txt")
    write_modif_file()
    re_minify_file()
    print("\nSteam Library JS Tweaks applied successfully.")
    time.sleep(2)
                
if __name__ == "__main__":
    main()
