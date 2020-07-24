#libraries needed: jsbeaitifier, jsmin

import jsbeautifier
import os.path
import sys
from jsmin import jsmin

if not os.path.isfile("libraryroot.beaut.js"):
    print("Opening JS file and beautifying...")
    library = jsbeautifier.beautify_file("libraryroot.js")
    #library = jsbeautifier.beautify_file("librarytest.js")

    f = open("libraryroot.beaut.js", "wt", newline='', encoding="UTF-8")
    print("Writing beautified file... please do not close")
    f.write(library)
    f.close()
    print("Beautified file write finished")


       
# LIST OF FIXES/TWEAKS
replacements = {'4:"libraryroot"}[n=u]||n': '4:"libraryreet"}[n=u]||n'}

'''
fixes_dict = {
    'Child: d,': 'Child: d,',
    'gridColumnGap: 16,': 'gridColumnGap: 5,',
    'gridRowGap: 24,': 'gridRowGap: 8,',
    'name : "library_600x900.jpg", e.rt': 'name : "header.jpg", e.rt',
    '[$o.GetCachedVerticalCapsuleURL(this.props.app), $o.GetVerticalCapsuleURLForApp(this.props.app),': \
    '[$o.GetCachedLandscapeImageURLForApp(this.props.app), $o.GetLandscapeImageURLForApp(this.props.app),',
    't + "/portrait.png?v=2"': 't + "/header.jpg"',
    'vecScreenShots.slice(0, 4).map': 'vecScreenShots.slice(0, 9).map',
    't = t.slice(0, 6),': 't = t.slice(0, 12),',
    'rowHeight: 90,': 'rowHeight: 40,'
}
'''
fixes_dict = {}

#modify library.js to look for different libraryroot.js file
def setup_library():
    lines = []
    with open('library.js') as infile:
        for line in infile:
            for src, target in replacements.items():
                line = line.replace(src, target)
            lines.append(line)
    with open('library.js', 'w') as outfile:
        for line in lines:
            outfile.write(line)
    infile.close()
    outfile.close()

def parse_fixes_file(filename):
    with open("fixes.txt", newline='', encoding="UTF-8") as fi:
        try:
            for line in fi:
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
