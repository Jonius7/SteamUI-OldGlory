#libraries needed: jsbeaitifier, jsmin

import jsbeautifier
import os.path
from jsmin import jsmin

if not os.path.isfile("libraryroot.beaut.js"):
    print("Opening file...")
    library = jsbeautifier.beautify_file("libraryroot.js")
    #library = jsbeautifier.beautify_file("librarytest.js")

    f = open("libraryroot.beaut.js", "wt", newline='', encoding="UTF-8")
    print("Writing beautified file... please do not close")
    f.write(library)
    f.close()
    print("Beautified file write finished")


       
# LIST OF FIXES/TWEAKS
replacements = {'4:"libraryroot"}[n=u]||n': '4:"libraryreet"}[n=u]||n'}

fixes_dict = {
    'Child: d,': 'Child: d,',
    'name : "library_600x900.jpg", e.rt': 'name : "header.jpg", e.rt',
    '[$o.GetCachedVerticalCapsuleURL(this.props.app), $o.GetVerticalCapsuleURLForApp(this.props.app),': \
    '[$o.GetCachedLandscapeImageURLForApp(this.props.app), $o.GetLandscapeImageURLForApp(this.props.app),',
    't + "/portrait.png?v=2"': 't + "/header.jpg"',
    'vecScreenShots.slice(0, 4).map': 'vecScreenShots.slice(0, 9).map',
    't = t.slice(0, 6),': 't = t.slice(0, 12),',
    'rowHeight: 90,': 'rowHeight: 40,'}


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


def find_fix(line, fix):
    m_line = line.replace(fix, fixes_dict[fix])
    print("FOUND")
    print(m_line)
    return m_line

def re_minify():
    with open("libraryroot.modif.js", "r", newline='', encoding="UTF-8") as js_file:
        minified = jsmin(js_file.read())
    with open("libraryreet.js", "w", newline='', encoding="UTF-8") as js_min_file:
        js_min_file.write(minified)
    js_file.close()
    js_min_file.close()
  
def main():
    setup_library()
    print("Finding Fixes")

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
