#JS Tweaker for Steam Library UI by Jonius7
#libraries needed: jsbeautifier, jsmin


import jsbeautifier
import os.path
import sys
from jsmin import jsmin

   
swap_js = {'"libraryroot"}[n=u]||n': '"libraryreet"}[n=u]||n'}

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
    lines = []
    with open('library.js') as infile:
        for line in infile:
            for src, target in swap_js.items():
                line = line.replace(src, target)
            lines.append(line)
    with open('library.js', 'w') as outfile:
        for line in lines:
            outfile.write(line)
    infile.close()
    outfile.close()

def parse_fixes_file(filename):
    with open("fixes.txt", newline='', encoding="UTF-8") as fi:
        lines = filter(None, (line.rstrip() for line in fi))
        try:
            for line in lines:
                if not line.startswith('###'):
                    (key, val) = line.rstrip().split("  ")
                    fixes_dict[key] = val
        except Exception as e:
            fi.close()
            print(e)
            sys.exit("Invalid file format")
    fi.close()
    #print(fixes_dict)

def find_fix(line, fix):
    m_line = line.replace(fix, fixes_dict[fix])
    print("FIX: ", end = '')
    print(m_line.strip())
    return m_line

def re_minify():
    with open("libraryroot.modif.js", "r", newline='', encoding="UTF-8") as js_file:
        minified = jsmin(js_file.read())
    with open("libraryreet.js", "w", newline='', encoding="UTF-8") as js_min_file:
        js_min_file.write(minified)
    js_file.close()
    js_min_file.close()
    print("Re-minify JS file")
  
def main():
    beautify_js()
    setup_library()
    print("Finding Fixes")
    parse_fixes_file("fixes.txt")
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
    re_minify()
                
if __name__ == "__main__":
    main()
