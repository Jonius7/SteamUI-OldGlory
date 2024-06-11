#JS Tweaker for Steam Library UI by Jonius7
#libraries needed: jsbeautifier, jsmin

import jsbeautifier
import js_beautify
import yaml
import os
import sys
import shutil
import traceback
import re
import rjsmin
import time
import copy
from rich import print as r_print

import backend

LOCAL_DEBUG = 0 #Set to 1 to not copy files to/from Steam directory
VERBOSE = 1

fixes_dict = {}

json_data = backend.get_json_data()


def initialise():
    fixes_dict.clear() #not fixes_dict = {}

######

files_to_copy = [json_data["libraryjsFile"], json_data["libraryrootjsFile"], json_data["jsFile"]]

def copy_files_from_steam(reset=0): #set reset to 1 to overwrite files with fresh copy (useful for updates)
    try:
        if reset == 1 or LOCAL_DEBUG == 1:
            for filename in files_to_copy:
                if os.path.exists(backend.library_dir() + "/" + filename):
                    print("Copying file " + filename + " from Steam\steamui...")
                    shutil.copy2(backend.library_dir() + "/" + filename, filename)
            
    except FileNotFoundError:
        error_exit("Steam directory and/or files not found.\n" \
              "Please check Steam\steamui for library.js and libraryroot.js")

def backup_files_from_steam():
    try:
        for filename in files_to_copy:
            #if os.path.exists(library_dir() + "/" + filename):
            #    shutil.copy2(library_dir() + "/" + filename, library_dir() + "/" + filename + ".original")
            if not os.path.exists(filename + ".original") and os.path.exists(backend.library_dir() + "/" + filename):
                shutil.copy2(backend.library_dir() + "/" + filename, filename + ".original")
    except:
        error_exit("Error while copying files")
            
def get_beaut_filename(filename):
    beaut_filename = filename.rsplit(".", 1)
    return beaut_filename[0] + ".beaut." + beaut_filename[1]

def get_modif_filename(filename):
    modif_filename = filename.rsplit(".", 1)
    return modif_filename[0] + ".modif." + modif_filename[1]

def beautify_js(filename=json_data["libraryrootjsFile"]):
    try:
        beautify_file = get_beaut_filename(filename)
        if not os.path.isfile(beautify_file) and os.path.isfile(os.path.join(backend.library_dir(), filename)):
            print("Opening " + beautify_file + ", generating beautified JS...")
            if not os.path.isfile(filename):
                shutil.copy2(os.path.join(backend.library_dir(), filename), filename)

            #opts = jsbeautifier.default_options()
            #library = jsbeautifier.beautify_file(filename, opts)
            #f = open(beautify_file, "wt", newline='', encoding="UTF-8")
            #f.write(library)
            #f.close()
            
            js_beautify.beautify(filename)
            
            print("Beautified file write finished")
    except:
        error_exit(filename + " not found")

def unpack_js(filename=json_data["libraryrootjsFile"]):
    try:
        print("Beautify file...")
        beautify_file = get_beaut_filename(filename)
        opts = jsbeautifier.default_options()
        library = jsbeautifier.beautify_file(filename, opts)
        f = open(beautify_file, "wt", newline='', encoding="UTF-8")
        f.write(library)
        f.close()
        print("Beautified file write finished")
        
    except:
        error_exit(filename + " not found")
    

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
        with open(backend.library_dir() + "/index.html", encoding="UTF-8") as infile:
            for line in infile:
                for src, target in html_array.items():
                    new_line = re.sub(src, target, line)
                    if new_line != line:
                        modified = 1
                lines.append(new_line)
        infile.close()
        if modified == 1:
            with open(backend.library_dir() + "/index.html.temp", 'w', encoding="UTF-8") as outfile:
                for line in lines:
                    outfile.write(line)            
            outfile.close()
            
            shutil.move(backend.library_dir() +"/index.html", backend.library_dir() + "/index.html.original")
            shutil.move(backend.library_dir() +"/index.html.temp", backend.library_dir() + "/index.html")
            print("index.html changing to use tweaked JS.")
            print("index.html backup created at " + backend.library_dir() + "/index.html.original")
    except:
        error_exit("index.html unable to be patched.")

def reset_html():
    try:
        if os.path.isfile(backend.library_dir() + "/index.html.original"):
            shutil.move(backend.library_dir() + "/index.html.original", backend.library_dir() + "/index.html")
            print(backend.library_dir() + "/index.html replaced with backup: " + "index.html.original")
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

# v2 handling tools Start

class YamlHandler:
    def __init__(self, filename):
        '''
        self.parse_yaml_file()
        '''
        self.filename = filename
        self.data = self.parse_yaml_file()
        self.f_data = None#self.format_yaml_data()
        
    def parse_yaml_file(self):
        with open(self.filename, newline='', encoding="UTF-8") as f:
            data = yaml.safe_load(f)
        f.close()
        return data
    
    def format_yaml_data(self, data):
        '''
        Format yaml file data to support Regex operations \n
        Requires functions in ConfigJSHandler to be run first to format data properly
        '''
        f_data = copy.deepcopy(data)
        self.regex = RegexHandler()
        for filename in f_data:
            for tweak in f_data[filename]:
                try:
                    for i, find_repl in enumerate(tweak_strs := f_data[filename][tweak]["strings"]):
                        #if using "previous line"
                        if (sem := semantic_find_str(find_repl["find"])):
                            tweak_strs[i].update({"find":
                                {"prev": self.regex.sub_find_with_regex(sem["prev"]),
                                "current": self.regex.sub_find_with_regex(sem["current"])}
                            })
                            tweak_strs[i]["repl"] = self.regex.sub_repl_with_regex(tweak_strs[i]["repl"])
                        else:
                            tweak_strs[i]["find"] = self.regex.sub_find_with_regex(tweak_strs[i]["find"])
                            tweak_strs[i]["repl"] = self.regex.sub_repl_with_regex(tweak_strs[i]["repl"])
                except KeyError:
                    print("Tweak " + tweak + " has no strings to find and replace, skipping", file=sys.stderr)
                    continue
                except:
                    error_exit("Unable to properly format Yaml data at: " + tweak)
        self.f_data = f_data
        if VERBOSE == 1:
            r_print(self.f_data)
        
    def format_yaml_data_compiled(self, data):
        '''
        Format yaml file data to support Regex operations \n
        Requires functions in ConfigJSHandler to be run first to format data properly
        '''
        f_data = copy.deepcopy(data)
        self.regex = RegexHandler()
        for filename in f_data:
            for tweak in f_data[filename]:
                try:
                    for i, find_repl in enumerate(tweak_strs := f_data[filename][tweak]["strings"]):
                        #if using "previous line"
                        if (sem := semantic_find_str(find_repl["find"])):
                            tweak_strs[i].update({"find":
                                {"prev": re.compile(self.regex.sub_find_with_regex(sem["prev"])),
                                "current": re.compile(self.regex.sub_find_with_regex(sem["current"]))}
                            })
                            tweak_strs[i]["repl"] = self.regex.sub_repl_with_regex(tweak_strs[i]["repl"])
                        else:
                            tweak_strs[i]["find"] = re.compile(self.regex.sub_find_with_regex(tweak_strs[i]["find"]))
                            tweak_strs[i]["repl"] = self.regex.sub_repl_with_regex(tweak_strs[i]["repl"])
                except KeyError:
                    print("Tweak " + tweak + " has no strings to find and replace, skipping", file=sys.stderr)
                    continue
                except:
                    error_exit("Unable to properly format Yaml data at: " + tweak)
        self.f_data = f_data
        if VERBOSE == 1:
            r_print(self.f_data)
    
    def r_print_to_file(self, data):
        '''
        prints dictionary of data to file, for visibility/checking
        '''
        pass

def raw_text(str_text):
    '''
    may not be needed \n
    takes a string and return a "raw string" version of it
    '''
    raw_text = [str_text]
    str_text = "%r"%str_text
    raw_text = str_text[1:-1]
    return raw_text

def escaped_pattern(pattern_str):
    '''
    Returns Regex escaped string
    '''
    #str = re.sub('\\\\([0-9]+)', '\\1', str)
    return re.escape(pattern_str)

def regex_search(pattern_str, string):
    return re.search(escaped_pattern(pattern_str), string)

def semantic_find_values(str, config):
    '''
    String to search through and find values
    '''
    pass

def semantic_find_str(find_str):
    '''
    May need to redo/realign with the process
    '''
    #find_str = unescape(find_str)
    semantic = None
    if "~~" in find_str:
        t = find_str.split("~~")
        if len(t) == 2:
            semantic = {"prev" : t[0],
                        "current" : t[1]}
    return semantic

def unescape(string):
    #new_string = re.sub(r'\\(.)', r'\1', string)
    #new_string = re.sub(r'\([tnrvf])', r'\1', string)
    #return new_string
    #should cover all practical cases
    new_string = re.sub(r'\\(.)', r'\1', string, flags=re.DOTALL)
    return new_string

class RegexHandler:
    def __init__(self):
        #Detecting variables %1% %2% %3% etc.
        self.vars_pattern = re.compile("%([0-9]+)%")
        self.refs_pattern = re.compile("%([a-z]+)%")
        #The regex pattern to replace them with
        self.js_letters = "([A-Za-z_$]{1,2})"
    
    def sub_find_with_regex(self, find):
        r'''
        returns string where:
            self.vars       regex pattern substituted with
            self.latters    regex pattern
        string special characters are escaped beforehand
            special characters: ()[]{}?*+-|^$\\.&~# \t\n\r\v\f
        '''
        return self.vars_pattern.sub(self.js_letters, escaped_pattern(find))
    
    def sub_repl_with_regex(self, repl):
        return self.vars_pattern.sub(r"\\"+"\\1",  escaped_pattern(repl))
    
    def sub_ref_with_regex(self, ref):
        return self.refs_pattern.sub(self.js_letters, escaped_pattern(ref))
    
    #def sub_extras_with_letters(self, extra_ref, letters):
    #    letters_iter = iter(letters)
    #    return self.refs_pattern.sub(self.match_letters(letters_iter), extra_ref)
    
    #def match_letters(self, letters_iter):
    #    return letters_iter.next()
    
    def find_and_repl(self, find, repl, line, lineno):
        '''
        takes a find/replace pair and returns the string to be written
            find - the string to find (regex formatted) \n
            repl - the string to replace it with (regex formatted) \n
            line - the line in question (in the tweaks file) \n
            unescape(re.sub(...))
        '''
        return_string = unescape(re.sub(find, repl, line))
        #print(return_string.ljust(70)[:70].strip() + (' ...' if len(return_string) > 70 else ''))
        print("TWEAK (" + str(lineno) + "): " + return_string.strip().ljust(120)[:120] + (' ...\n' if len(return_string) > 120 else '\n'), end='')
        return return_string 
    
    def compiled_find_and_repl(self, find, repl, line, lineno):
        '''
        takes a find/replace pair and returns the string to be written
            find - the compiled string to find (regex formatted) \n
            repl - the string to replace it with (regex formatted) \n
            line - the line in question (in the tweaks file) \n
            unescape(re.sub(...))
        '''
        return_string = unescape(find.sub(repl, line))
        #print(return_string.ljust(70)[:70].strip() + (' ...' if len(return_string) > 70 else ''))
        print("TWEAK (" + str(lineno) + "): " + return_string.strip().ljust(120)[:120] + (' ...\n' if len(return_string) > 120 else '\n'), end='')
        return return_string    
        
    def find(self, find, line):
        '''
        - find: pattern
        - line: text to search \n
        re.search(...)
        '''
        return re.search(find, line)
    
    def compiled_find(self, find, line):
        '''
        - find: compiled pattern
        - line: text to search \n
        re.search(...)
        '''
        return find.search(line)



# v2 handling tools end


        

def write_modif_file(filename = json_data["libraryrootjsFile"]):
    beaut_filename = get_beaut_filename(filename)
    modif_filename = get_modif_filename(filename)
    try:
        if os.path.exists(beaut_filename):
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

def re_minify_file(modif_filename = json_data["libraryrootjsModifFile"],
                   min_filename = json_data["libraryrootjsPatchedFile"]):
    '''
    Previously minified JS files until it stopped working
    '''
    try:
        if os.path.isfile(modif_filename):
            '''
            print("\nRe-minify JS file")
            with open(modif_filename, "r", newline='', encoding="UTF-8") as js_file:
                minified = rjsmin.jsmin(js_file.read(), keep_bang_comments=True)
            with open(min_filename, "w", newline='', encoding="UTF-8") as js_min_file:
                js_min_file.write(minified)
            js_file.close()
            js_min_file.close()
            print("JS Minify complete. (" + min_filename + ")")
            '''
            shutil.copy2(modif_filename, min_filename)
            print("File " + modif_filename + " copied to " + min_filename)
            
    except:
        error_exit("Error completing JS minify.")

def compress_newlines(filename = "librery.js"):
    if os.path.isfile(filename):
        with open(filename, encoding="UTF-8") as f1, \
            open(filename + ".compress", "w", newline='', encoding="UTF-8") as f2:
            output = " ".join(f1.read().splitlines())
            f2.write(output)
        f1.close()
        f2.close()

        os.remove(filename)
        shutil.move(filename + ".compress", filename)       

#was hardcoded values
def copy_files_to_steam():
    try:
        if LOCAL_DEBUG == 0:
            files_to_copy = {json_data["libraryjsPatchedFile"]: json_data["libraryjsPatchedFile"],
                             json_data["libraryrootjsPatchedFile"]: json_data["libraryrootjsPatchedFile"],
                             json_data["jsPatchedFile"]: json_data["jsPatchedFile"]}
            for filename in files_to_copy:
                if os.path.isfile(filename):
                    shutil.copy2(filename, backend.library_dir() + "/" + files_to_copy[filename])
                    print("File " + filename + " written to " + backend.library_dir() + "/" + files_to_copy[filename])
                
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
