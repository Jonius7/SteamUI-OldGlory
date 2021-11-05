'''
js_manager.py\n
For anytoshing js_tweaker needs to access from other OldGlory modules\n

libraries needed: schema
'''

import os
import old_glory
import backend
import js_tweaker

import sys
import traceback
import re
from schema import Schema, Optional, Use, SchemaError, SchemaWrongKeyError
import datetime

class ValuesJSHandler:
    pass

class ConfigJSHandler:
    '''
    data            Yaml data, from yaml.safe_load(f)
    config          config dictionary, from the likes of backend.load_config()
    f_data_by_file  Filtered Yaml data (split by file, enabled tweaks only)
    '''
    def __init__(self, data, config):
        self.default = "libraryroot.js"
        self.reg_value = re.compile("(@[A-Za-z]+@)")
        
        self.data = data
        self.config = config
        self.f_data_by_file = self.get_js_enabled_data_by_file()
        self.f_data_by_file = self.populate_data()
        self.refs_data = self.get_refs_data(self.f_data_by_file)
        
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
        
    def populate_data(self, f_data_by_file=None):
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
            Optional('refs'): [str],
            Optional('values'): [str],
            Optional('file'): str
            }}}, ignore_extra_keys=True)
        try:
            return js_tweaks_schema.validate(data)
        except SchemaError:
            js_tweaker.print_error("Invalid JS Tweaks File Format. \n" \
                  'Please check your file includes the required "name" and "strings" attributes for each tweak.')
    
    def get_refs_data(self, data):
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
        and returns a version of refs_data with these variables
        '''
        try:
            if refs_data is None:
                refs_data = self.refs_data
            r_search = js_tweaker.RegexHandler()
            refs_dict = {}
            
            rgx_refs_data = self.get_regex_refs(refs_data)
            #print(rgx_refs_data)
            #rgx_refs_queue = self.get_regex_ref_queue(refs_data)
            #print(rgx_refs_queue)

            
            for filename in rgx_refs_data:
                beaut_filename = self.get_beaut_filename(filename)
                if os.path.exists(beaut_filename):
                    refs_queue = []
                    for rgx_ref in rgx_refs_data[filename]:
                        refs_queue.append(rgx_ref)
                    #print ("WAGOINSEGSE")
                    #print (refs_queue)
                        
                    with open(beaut_filename, "r", newline='', encoding="UTF-8") as f:
                        for line in f:
                            #print(line)
                            for rgx_ref in refs_queue:
                                #print(rgx_ref)
                                if (match := r_search.find(rgx_ref, line)):
                                    print(match.group(0))
                                    #print("FOUND")
                    
                else:
                    print("File " + beaut_filename + " does not exist, skipping.")
                    
            '''
            for filename in rgx_refs_data:
                    refs_queue = self.get_refs_for_file(filename, rgx_refs_data[filename])
                    with open(filename, "r", newline='', encoding="UTF-8") as f:
                        for line in f:
                            for i, ref in enumerate(refs_queue):
                                if (match := r_search.find(ref, line)):
                                    #print(match)
                                    rgx_refs_data[filename][tweak]["refs"] = match.group(0)
                                    refs_queue.remove(ref)
                    f.close() 
            '''           
                
            '''
            with open(filename, "r", newline='', encoding="UTF-8") as f:
                for line in f:
                    for i, ref in enumerate(rgx_refs_data):
                        if (match := r_search.find(ref, line)):
                            #print(match)
                            refs_dict[refs_data[i]] = match.group(0)
                            rgx_refs_data.remove(ref)
            f.close()
            return refs_dict'''
                   
            
        except:
            js_tweaker.error_exit("Error while searching for Refs")
    
    def get_beaut_filename(self, original_filename):
        '''
        eg:
            original_filename   - libraryroot.js
            beaut_filename      - libraryroot.beaut.js
        '''
        (name, ext) = os.path.splitext(original_filename)
        return name + "." + "beaut" + ext
           
    def get_regex_refs(self, refs_data):
        '''
            param refs_data
                format: {filename: {tweak: "refs": [ref1, ref2]}}
            
            returns rgx_refs_data
                format: {"filename": 
                    {ref1: {"regex": rgx_ref1, "tweak": tweak}}, 
                    {ref2: {"regex": rgx_ref2, "tweak": tweak}}}
        '''
        r_search = js_tweaker.RegexHandler()
        rgx_refs_data = {}
        for filename in refs_data:
            for tweak in refs_data[filename]:
                if "refs" in refs_data[filename][tweak]:
                    for i, ref in enumerate(refs_data[filename][tweak]["refs"]):
                        #print(r_search.sub_ref_with_regex(ref))

                        rgx_refs_data.setdefault(filename, {})[r_search.sub_ref_with_regex(ref)] \
                            = {"original": ref, "tweak": tweak}
        return rgx_refs_data
    
    def get_refs_for_file(self, filename, file_refs_data):
        '''
            file_refs_data - {
                {ref1: {"regex": rgx_ref1, "tweak": tweak}},
                {ref2: {"regex": rgx_ref2, "tweak": tweak}}}
        '''
        
        
        
        return None

        #return {tweak_k : tweak_v for (tweak_k, tweak_v) in file_refs_data.items()}
    
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
        print(tweak_data)
        for find_repl in tweak_data["strings"]:
            for value in tweak_data["values"]:
                find_repl["repl"] = find_repl["repl"].replace(
                    "@" + value + "@",
                    self.get_js_value_from_config(value))
                #print(find_repl["repl"]) 
        return tweak_data
    
    def get_line(self, data_dict):
        for k, v in data_dict.items():
            if isinstance(v, dict):
                data_dict[k] = self.get_line(self, v)
            else:
                return re.sub(self.reg_value, )
            
def process_yaml():
    y_handler = js_tweaker.YamlHandler("js_tweaks.yml")
    c_handler = ConfigJSHandler(y_handler.data, backend.load_config())
    c_handler.f_data_by_file = c_handler.populate_data()
    
    return c_handler

    #add refs
    #sub regex
    #escape characters