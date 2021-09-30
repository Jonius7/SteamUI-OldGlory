'''
js_manager.py\n
For anything js_tweaker needs to access from other OldGlory modules\n

libraries needed: jsbeautifier, jsmin
'''

import old_glory
import backend

import sys

class ValuesJSHandler:
    pass

class ConfigJSHandler:
    '''
        f_data  formatted Yaml data, from the likes of js_tweaker.YamlHandler.format_yaml_data()
        config  config dictionary, from the likes of backend.load_config()
    '''
    def __init__(self, f_data, config):
        self.default = "libraryroot.js"
        self.f_data = f_data
        self.config = config
        self.f_data_list = self.get_js_enabled_data_by_file()
        
    def get_js_enabled_data_by_file(self):
        f_data_list = {self.default: {}}
        for tweak in self.f_data:
            try:
                if True:#tweak in self.config["JS_Settings"] and self.config["JS_Settings"][tweak] == '1':
                    #The dictionary containing 1 tweak's data
                    tweak_data = self.f_data[tweak]
                    if "file" not in tweak_data:
                        print ("USING DEFAULT for: " + tweak)
                        f_data_list[self.default][tweak] = tweak_data
                    else:
                        if tweak_data["file"] not in f_data_list:
                            f_data_list[tweak_data["file"]] = {}
                        f_data_list[tweak_data["file"]][tweak] = tweak_data
                                                
            except KeyError:
                print("Tweak " + tweak + " has no strings to find and replace, skipping", file=sys.stderr)
                continue
        return f_data_list