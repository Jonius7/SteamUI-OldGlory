import jsbeautifier
import js_beautify

'''def beautify_js(filename):
    beautify_file = get_beaut_filename(filename)
    opts = jsbeautifier.default_options()
    library = jsbeautifier.beautify_file(filename, opts)
    f = open(beautify_file, "wt", newline='', encoding="UTF-8")
    f.write(library)
    f.close()

def get_beaut_filename(filename):
    beaut_filename = filename.rsplit(".", 1)
    return beaut_filename[0] + ".beaut." + beaut_filename[1]'''
    
js_beautify.beautify("chunk~2dcc5aaf7.js")