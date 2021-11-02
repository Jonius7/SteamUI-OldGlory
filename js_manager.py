'''
js_manager.py\n
For anytoshing js_tweaker needs to access from other OldGlory modules\n

libraries needed: schema
'''

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
        
    def get_js_enabled_data_by_file(self):
        f_data_by_file = {self.default: {}}
        for tweak in self.data:
            try:
                if tweak in self.config["JS_Settings"] and self.config["JS_Settings"][tweak] == '1':
                    print("Tweak Enabled " + tweak)
                    #The dictionary containing 1 tweak's data
                    tweak_data = self.data[tweak]
                    if "file" not in tweak_data:
                        print ("  USING DEFAULT " + self.default + " for: " + tweak)
                        f_data_by_file[self.default][tweak] = tweak_data
                    else:
                        #if the filename doesn't exist yet in dict, create it
                        if tweak_data["file"] not in f_data_by_file:
                            f_data_by_file[tweak_data["file"]] = {}
                        f_data_by_file[tweak_data["file"]][tweak] = tweak_data
                else:
                    print("NOT ENABLED " + tweak)
                                                
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
    
    def refs_dict(self, data):
        '''
        refs_schema = Schema({str: {str: {
            'name': str,
            'strings': [{'find': str, 'repl': str}],
            'refs': [str],
            }}}, ignore_extra_keys=True)
        try:
            return refs_schema.validate(data)
        except SchemaError:
            js_tweaker.print_error("Invalid ref searching")
        '''
        subset = {"refs", "file", "strings"}        
        
        refs_data = {filename_k : {tweak_k : {attr_k : attr_v
                for (attr_k, attr_v) in tweak_v.items() if attr_k in subset}             
                for (tweak_k, tweak_v) in filename_v.items() if (tweak_v.keys for sub in subset)} 
                for (filename_k, filename_v) in data.items()}
        
        return refs_data
    
    def search_for_refs(self, filename, ref_queue):    
        try:
            r_search = js_tweaker.RegexHandler()
            ref_dict = {}
            rgx_ref_queue = self.get_regex_ref_queue(ref_queue)
            with open(filename, "r", newline='', encoding="UTF-8") as f:
                for line in f:
                    for i, ref in enumerate(rgx_ref_queue):
                        if (match := r_search.find(ref, line)):
                            #print(match)
                            ref_dict[ref_queue[i]] = match.group(0)
                            rgx_ref_queue.remove(ref)
            f.close()
            return ref_dict
        except:
            js_tweaker.error_exit("Error while searching for Refs")
                    
    def get_regex_ref_queue(self, ref_queue):
        rgx_ref_queue = []
        rgx = js_tweaker.RegexHandler()
        for i, ref in enumerate(ref_queue):
            rgx_ref_queue.append(rgx.sub_ref_with_regex(ref_queue[i]))
        return rgx_ref_queue
    
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

    #add refs
    #sub regex
    #escape characters