'''
js_manager.py\n
For anything js_tweaker needs to access from other OldGlory modules\n

libraries needed: schema
'''

import os
import sys
import traceback
import re
from schema import Schema, Optional, Use, SchemaError, SchemaWrongKeyError
import datetime
from collections import Counter
from rich import print as r_print

#import old_glory
import backend
import js_tweaker

class ValuesJSHandler:
    pass

class ConfigJSHandler:
    '''
    data            Yaml data, from yaml.safe_load(f)
    config          config dictionary, from the likes of backend.load_config()
    f_data_by_file  Filtered Yaml data (split by file, enabled tweaks only)
    '''
    def __init__(self, data, config):
        '''
        self.get_js_enabled_data_by_file()
        self.populate_data_values()
        self.get_refs_data(self.f_data_by_file)
        self.get_ref_letters()
        '''
        self.default = "libraryroot.js"
        self.reg_value = re.compile("(@[A-Za-z]+@)")
        
        self.data = data
        self.config = config
        self.f_data_by_file = self.get_js_enabled_data_by_file()
        self.f_data_by_file = self.populate_data_values()
        self.refs_data = self.get_refs_data(self.f_data_by_file)
        self.ref_letters = self.get_ref_letters()
        
        self.REFS_LIMIT = 20
        self.REFS_EXTRAS_LIMIT = 20
        
    def get_js_enabled_data_by_file(self):
        f_data_by_file = {self.default: {}}
        for tweak in self.data:
            try:
                if tweak in self.config["JS_Settings"] and self.config["JS_Settings"][tweak] == '1':
                    #print("Tweak Enabled " + tweak)
                    #The dictionary containing 1 tweak's data
                    tweak_data = self.data[tweak]
                    if "file" not in tweak_data:
                        #print ("  USING DEFAULT " + self.default + " for: " + tweak)
                        f_data_by_file[self.default][tweak] = tweak_data
                    else:
                        #if the filename doesn't exist yet in dict, create it
                        if tweak_data["file"] not in f_data_by_file:
                            f_data_by_file[tweak_data["file"]] = {}
                        f_data_by_file[tweak_data["file"]][tweak] = tweak_data
                else:
                    #print("NOT ENABLED " + tweak)
                    pass                               
            except KeyError:
                print("Tweak " + tweak + " has no strings to find and replace, skipping", file=sys.stderr)
                continue
        return f_data_by_file
    
    def get_js_value_from_config(self, value_name):
        if value_name in self.config["JS_Values"]:
            return self.config["JS_Values"][value_name]
        else:
            return "0"
        
    def populate_data_values(self, f_data_by_file=None):
        '''
        Takes the JS data and returns a version of it with values put in
        '''
        if f_data_by_file is None:
            f_data_by_file = self.f_data_by_file
        validated_data = self.schema_validate(f_data_by_file)
        
        if isinstance(validated_data, dict):
            for filename in validated_data:
                for tweak in validated_data[filename]:
                    if "values" in validated_data[filename][tweak]:
                        validated_data[filename][tweak] = self.replace_js_values(validated_data[filename][tweak])
                        #print(validated_data[filename][tweak])
        else:
            print("Something unexpectedly went wrong with the JS Tweaks data.", file=sys.stderr)
        return validated_data
    
    def schema_validate(self, data):
        js_tweaks_schema = Schema({str: {str: {
            'name': str,
            'strings': [{'find': str, 'repl': str}],
            Optional('desc'): str,
            Optional('category'): str,
            Optional('refs'): [str,[str]],
            Optional('values'): [str],
            Optional('file'): str
            }}}, ignore_extra_keys=True)
        try:
            return js_tweaks_schema.validate(data)
        except SchemaError:
            js_tweaker.print_error("Invalid JS Tweaks File Format. \n" \
                  'Please check your file includes the required "name" and "strings" attributes for each tweak.')
    
    def get_refs_data(self, data):
        '''
        returns dictionary containing tweaks that only have refs attrs
        '''
        subset = {"refs"}        
        
        #create dictionary containing tweaks that only have refs attrs
        refs_data = {filename_k : {tweak_k : {attr_k : attr_v
                for (attr_k, attr_v) in tweak_v.items() if attr_k in "refs"}             
                for (tweak_k, tweak_v) in filename_v.items() if self.refs_in_tweak(tweak_v.keys(), subset)} 
                for (filename_k, filename_v) in data.items()}
        
        return refs_data
    
    def refs_in_tweak(self, keys, subset):
        for sub in subset:
            if sub in keys:
                return True
            else:
                return False
        
    def search_for_refs(self, refs_data=None):
        '''
        Uses refs_data to search for the right obfuscated variables in js files
        and returns a version of refs_data with these variables \n
        param refs_queue
            format: [rgxref1, rgxref2, rgxref3 ...]
        param refs_results
            format: {rgx_ref: [result1, result2, result3 ...]}
        returns rgx_refs_data
            format: {filename: {
                rgx_ref1: {'original': ref1, 'tweak': tweak_name1, 'realtext': freq_ref1, 'letters': ('a', 'b', 'c' ...), 'extra': [{extra_ref1: extra_ref_realtext1},]},
                rgx_ref2: {'original': ref2, 'tweak': tweak_name2, 'realtext': freq_ref2, 'letters': ('a', 'b', 'c' ...), 'extra': [{extra_ref1: extra_ref_realtext1},]}}
            }}
        '''
        try:
            if refs_data is None:
                refs_data = self.refs_data
            r_search = js_tweaker.RegexHandler()
            refs_dict = {}
            
            rgx_refs_data = self.get_regex_refs(refs_data)
            
            for filename in rgx_refs_data:
                beaut_filename = js_tweaker.get_beaut_filename(filename)
                if os.path.exists(beaut_filename):
                    refs_queue = []
                    refs_matches = {}
                    for rgx_ref in rgx_refs_data[filename]:
                        refs_queue.append(rgx_ref)
                        refs_matches[rgx_ref] = []

                    with open(beaut_filename, "r", newline='', encoding="UTF-8") as f:
                        for line in f:
                            for rgx_ref in refs_queue:
                                if (match := r_search.find(rgx_ref, line)):
                                    refs_matches[rgx_ref].append(match.group(0))
                                    #r_print("CAPTURE GROUPS")
                                    rgx_refs_data[filename][rgx_ref]['letters'] = match.groups()
                                    #r_print(rgx_refs_data[filename][rgx_ref]['letters'])
                    #r_print("debugging")
                    #r_print(refs_results)
                    freq_refs_results = self.get_most_freq_refs(refs_matches)
                    #r_print(freq_refs_results)
                    for (rgx_ref, freq_ref) in freq_refs_results.items():
                        rgx_refs_data[filename][rgx_ref]['realtext'] = freq_ref
                    for rgx_ref in rgx_refs_data[filename]:
                        #maximum 20 extra_refs to avoid overloading
                        if isinstance((extra_refs := rgx_refs_data[filename][rgx_ref]["extra"][:self.REFS_EXTRAS_LIMIT]), list):
                            extra_refs_realtexts = self.convert_extra_refs(extra_refs,
                                                                           rgx_refs_data[filename][rgx_ref]["letters"])
                            rgx_refs_data[filename][rgx_ref]["extra"] = \
                                [{extra_ref: extra_refs_realtexts[i]}
                                 for i, extra_ref in enumerate(extra_refs)]
                            #print(extra_refs)
                                
                       
                else:
                    print("File " + beaut_filename + " does not exist, skipping tweaks.")
            #r_print(rgx_refs_data) 
            #r_print(self.f_data_by_file)    
            return rgx_refs_data                  
            
        except:
            js_tweaker.error_exit("Error while searching for Refs")
            
    def get_most_freq_refs(self,refs_results):
        freq_refs_results = {rgx_ref_k : Counter(rgx_ref_v).most_common(1)[0][0]
                             for (rgx_ref_k, rgx_ref_v) in refs_results.items() if rgx_ref_v}
        return freq_refs_results
           
    def get_regex_refs(self, refs_data):
        '''
            param refs_data
                format: {filename: {tweak: "refs": [ref1, ref2]}}
            
            returns rgx_refs_data
                format: rgx_refs_data - {filename: {
                    rgx_ref1: {'original': ref1, 'tweak': tweak_name1, 'extra': [extra_ref1, extra_ref2 ...]},
                    rgx_ref2: {'original': ref2, 'tweak': tweak_name2, 'extra': [extra_ref1, extra_ref2 ...]}
                }}
        '''
        r_search = js_tweaker.RegexHandler()
        rgx_refs_data = {}
        for filename in refs_data:
            for tweak in refs_data[filename]:
                if "refs" in refs_data[filename][tweak]:
                    for i, ref in enumerate(refs_data[filename][tweak]["refs"][:self.REFS_LIMIT]):
                        #print(r_search.sub_ref_with_regex(ref))
                        
                        (first_ref, extra_refs) = self.split_refs_sublist(ref)
                        rgx_refs_data.setdefault(filename, {}) \
                            [r_search.sub_ref_with_regex(first_ref)] \
                            = {"original": first_ref, "tweak": tweak, "extra": extra_refs[:self.REFS_EXTRAS_LIMIT]}
        return rgx_refs_data
    
    def get_refs_for_file(self, filename, file_refs_data):
        '''
            file_refs_data - {
                {ref1: {"regex": rgx_ref1, "tweak": tweak}},
                {ref2: {"regex": rgx_ref2, "tweak": tweak}}}
        '''
        
        return None

        #return {tweak_k : tweak_v for (tweak_k, tweak_v) in file_refs_data.items()}
    
    def get_ref_letters(self):
        '''Returns list of ref letters
            ['%a%', '%b%', '%c%', ...]
        '''
        letters_key = "abcdefghijklmnopqrstuvwxyz"
        #letters_map = {"%" + letter + "%": ord(letter) - 96 for letter in letters_key}
        ref_letters = ["%" + letter + "%" for letter in letters_key]
        return ref_letters
    
    def convert_extra_refs(self, extra_refs, letters):
        new_extra_refs = []
        letters_map = {self.ref_letters[i]: letter for i, letter in enumerate(letters)}
        #for letter in letters:
        #    letters_map = self.dict_slice(self.ref_letters, len(letters))
        
        for ref in extra_refs:
            pattern = re.compile("|".join(letters_key for letters_key in letters_map))
            new_ref = pattern.sub(lambda x: letters_map[x.group(0)], ref)
            #new_ref = re.sub()
            #new_ref = (ref.replace(letters_key, letters_map, ref) for letters_key in letters_map)
            new_extra_refs.append(new_ref)
        
        return new_extra_refs
    
    def dict_slice(self, dict, number):
        '''Returns a slice (subset) of a dictionary up to number items'''
        return {k: v for (k, v) in dict.items() if v <= number}
            
    
    def populate_data_refs(self, rgx_refs_data, f_data_by_file=None):
        '''
        separate ref from extra refs, realtext setup
        modifies f_data_by_file given
        '''
        if f_data_by_file is None:
            f_data_by_file = self.f_data_by_file
            
        for filename in rgx_refs_data:
            for rgx_ref in rgx_refs_data[filename]:
                if (original_text := rgx_refs_data[filename][rgx_ref]["original"]) \
                    in self.get_first_refs(f_data_by_file[filename][rgx_refs_data[filename][rgx_ref]["tweak"]]["refs"]):
                    for find_repl in f_data_by_file[filename][rgx_refs_data[filename][rgx_ref]["tweak"]]["strings"]:
                        #print("REPLACING")
                        #print(originaltext)
                        find_repl["find"] = find_repl["find"].replace(original_text, rgx_refs_data[filename][rgx_ref]["realtext"])
                        find_repl["repl"] = find_repl["repl"].replace(original_text, rgx_refs_data[filename][rgx_ref]["realtext"])
                        #print(find_repl["repl"])
                        if isinstance(extra_refs := rgx_refs_data[filename][rgx_ref]["extra"], list):
                            for ref in extra_refs:
                                #print(ref)
                                (original, realtext), = ref.items() #unpack
                                find_repl["find"] = find_repl["find"].replace(original, realtext)
                                find_repl["repl"] = find_repl["repl"].replace(original, realtext)
                                
        
        #r_print(f_data_by_file)
                    
    def split_refs_sublist(self, ref_sublist):
        '''
        if a ref (sublist) is a list, return only the first ref
        '''
        if isinstance(ref_sublist, list) and ref_sublist:
            return (ref_sublist[0], ref_sublist[1:])
        else:
            return (ref_sublist, "")

    def get_first_refs(self, refs_list):
        first_refs_list = []
        for ref in refs_list:
            (first_ref, extra_refs) = self.split_refs_sublist(ref)
            first_refs_list.append(first_ref)
        return first_refs_list
                
    
    '''
    def get_regex_ref_queue(self, refs_data):
        r_search = js_tweaker.RegexHandler()
        rgx_ref_queue = []
        
        for filename in refs_data:
            for tweak in refs_data[filename]:
                if "refs" in refs_data[filename][tweak]:
                    for ref in refs_data[filename][tweak]["refs"]:
                        #print(r_search.sub_ref_with_regex(ref))
                        rgx_ref_queue.append(r_search.sub_ref_with_regex(ref))
        return rgx_ref_queue
    '''
    
    def replace_js_values(self, tweak_data):
        '''
        tweak_data  The dictionary containing 1 tweak's data
        '''
        #print(tweak_data)
        for find_repl in tweak_data["strings"]:
            for value in tweak_data["values"]:
                find_repl["repl"] = find_repl["repl"].replace(
                    "@" + value + "@",
                    self.get_js_value_from_config(value))
                #print(find_repl["repl"]) 
        return tweak_data
    
    
    '''def get_line(self, data_dict):
        for k, v in data_dict.items():
            if isinstance(v, dict):
                data_dict[k] = self.get_line(self, v)
            else:
                return re.sub(self.reg_value, )'''
           
def process_yaml():
    '''
    processes yaml through YamlHandler and ConfigJSHandler\n
    returns YamlHandler
    '''
    start_time = datetime.datetime.now()
    y_handler = js_tweaker.YamlHandler("js_tweaks.yml")
    c_handler = ConfigJSHandler(y_handler.data, backend.load_config())
    c_handler.f_data_by_file = c_handler.populate_data_values()
    c_handler.populate_data_refs(c_handler.search_for_refs())
    #return c_handler
    if not js_tweaker.COMPILED:
        y_handler.format_yaml_data(c_handler.f_data_by_file)
    elif js_tweaker.COMPILED:
        y_handler.format_yaml_data_compiled(c_handler.f_data_by_file)
    
    end_time = datetime.datetime.now()
    print("Process yaml time: " + str(end_time - start_time) + " seconds")
    return y_handler
    
    

    #add refs
    #sub regex
    #escape characters