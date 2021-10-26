import unittest
import sys
from pathlib import Path
sys.path.append(str(Path('.').absolute().parent))
import backend
import js_tweaker
import js_manager
import datetime
import re
from rich import print as r_print

#CSS Line Parser
class TestJSManager(unittest.TestCase):

    def test_get_js_by_file(self):
        self.y = js_tweaker.YamlHandler(sys.path[0] + "/../js_tweaks.yml")
        self.a = js_manager.ConfigJSHandler(self.y.f_data, backend.load_config())
        r_print(self.a.config)
        r_print(self.a.f_data_list)
        print("---")
        r_print(self.a.config.get('JS_Values')['ColumnSpacing'])
    
        
if __name__ == '__main__':
    unittest.main(exit=False)
