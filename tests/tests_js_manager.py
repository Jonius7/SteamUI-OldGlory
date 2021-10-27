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
    
    @classmethod
    def setUpClass(cls):
        cls.y = js_tweaker.YamlHandler(sys.path[0] + "/../js_tweaks.yml")
        cls.a = js_manager.ConfigJSHandler(cls.y.data, backend.load_config())        
        
    def test_get_js_by_file(self):
        r_print(self.a.config)
        r_print(self.a.f_data_by_file)
        print("---")
        r_print(self.a.config.get('JS_Values')['ColumnSpacing'])
        
    def test_get_js_values_not_found(self):
        self.assertEqual(self.a.get_js_value_from_config("DUMMY"), "0")
        
    def test_get_js_values_found_1(self):
        self.assertEqual(self.a.get_js_value_from_config("SmallGridSize"), "120")
    
        
if __name__ == '__main__':
    unittest.main(exit=False)
