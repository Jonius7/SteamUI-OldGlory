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
from schema import Schema, SchemaError

#CSS Line Parser
class TestJSManager(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.y = js_tweaker.YamlHandler(sys.path[0] + "/../js_tweaks.yml")
        cls.a = js_manager.ConfigJSHandler(cls.y.data, backend.load_config())        
        
    def test_get_js_by_file(self):
        #r_print(self.a.config)
        #r_print(self.a.f_data_by_file)
        print("---")
        r_print(self.a.config.get('JS_Values')['ColumnSpacing'])
        
    def test_get_js_values_not_found(self):
        self.assertEqual(self.a.get_js_value_from_config("DUMMY"), "0")
        
    def test_get_js_values_found_1(self):
        self.assertEqual(self.a.get_js_value_from_config("SmallGridSize"), "120")
        
    def test_full_process_yaml(self):
        js_manager.process_yaml()

class TestSchema(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.y = js_tweaker.YamlHandler(sys.path[0] + "/../js_tweaks.yml")
        cls.a = js_manager.ConfigJSHandler(cls.y.data, backend.load_config())
    
    #single key/value
    def test_schema_dummy1(self):
        schema = Schema({str: {str: {'name': str}}})
        data = {'libraryroot': {"DimUninstalled": {"name" : "DD"}}}
        schema.validate(data)
        #self.assertIsInstance(data, dict)
    
    #multiple key value
    def test_schema_dummy2(self):
        schema = Schema({str: {str: {'name': str}}})
        data = {'libraryroot': {"DimUninstalled": {"name" : "DD"}, "DimUninstalled2": {"name" : "EE"}}}
        schema.validate(data)
    
    #assert SchemaError
    def test_schema_dummy3(self):
        keyname = "DimUninstalled"
        schema = Schema({str: {str: {'name': str}}})
        data = {'libraryroot': {keyname: {"not" : "DD"}}}
        with self.assertRaises(SchemaError):
            schema.validate(data)
            
    def test_schema_validate1(self):
        validated = self.a.populate_data_values()
        #print(validated)
    
    #ignore extra keys
    def test_schema_validate2(self):
        data = {'libraryroot': {"DimUninstalled": {
            "name" : "DD",
            "EXTRAEXTRA": "This won't appear",
            "strings" : [{"find": 'grid', "repl": 'gride'}]}}}
        validated = self.a.populate_data_values(data)
        #print(validated)
        
    def test_schema_validate3(self):
        data = {'libraryroot': {"DimUninstalled": {
            "name" : "DD",
            "values" : ['SmallGridSize','MediumGridSize','LargeGridSize'],
            "EXTRAEXTRA": "This won't appear",
            "strings" : [{"find": 'grid', "repl": 'gride @SmallGridSize@'}]}}}
        validated = self.a.populate_data_values(data)
        #print(validated)
        
    #full data
    def test_schema_validate4(self):
        validated = self.a.populate_data_values()
        r_print(validated)
        self.assertEqual(validated['libraryroot.js']['HomePageGridSpacing']['strings'][0]['repl'], 'gridColumnGap: 5,')

class TestValues(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.y = js_tweaker.YamlHandler(sys.path[0] + "/../js_tweaks.yml")
        cls.a = js_manager.ConfigJSHandler(cls.y.data, backend.load_config())
        

    def test_add_values1(self):
        data = {
            "name" : "DD",
            "values" : ['SmallGridSize','MediumGridSize','LargeGridSize'],
            "strings" : [{"find": 'TEXT1 22', "repl": 'ANTITEXT @SmallGridSize@ @MediumGridSize@'}]}
        self.a.replace_js_values(data)
        #print(self.a.f_data_by_file)

class TestRefs(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.y = js_tweaker.YamlHandler(sys.path[0] + "/../js_tweaks.yml")
        cls.a = js_manager.ConfigJSHandler(cls.y.data, backend.load_config())
        cls.r = js_tweaker.RegexHandler()
        
    def test_search_refs1(self):     
        rf = self.a.search_for_refs(
            {'testbed.js': {'StickyBackgroundImage': {'refs': ['%a%.%b%.currentGameListSelection.nAppId']}}, 
             'library.js': {}})
        
        
    def test_search_refs2(self):   
        rf = self.a.search_for_refs(
            {'testbed.js': {'StickyBackgroundImage': {'refs': ['%a%.%b%.currentGameListSelection.nAppId','%c%.%d%.currensegsegtion.nAppId']}}, 
             'library.js': {'NOTEST': {'refs': ['%a%.%b%.currentGame3ListSelection.nAppId','%c%.%d%.currensegsegtion.nAppId']}}})

    def test_search_refs3(self):   
        rf = self.a.search_for_refs(
            {'testbed.js': {'StickyBackgroundImage': {'refs': ['%a%.%b%.SOMESELECTION.nAppId','%c%.%d%.NEXTSELECTION.nAppId']},
                                'NextBackgroundImage': {'refs': ['%a%.%b%.currentGameListSelection.nAppId','%c%.%d%.nextsection.nAppId']}}, 
             'library.js': {'NOTEST': {'refs': ['%a%.%b%.currentGame3ListSelection.nAppId','%c%.%d%.nextSSection.nAppId']}}})
        
    def test_search_refs4(self):
        rf = self.a.search_for_refs()
        
    def test_search_refs5(self):
        rf = self.a.search_for_refs(
            {'libraryroot.js': {'StickyBackgroundImage': {
                'refs': ['%a%.currentGameListSelection.nAppId', 
                         '(%a%.%b%)("#FacetedBrowse_ReturnToTop")))',
                         '%a%.%b%.EventDaySeparator',
                         '"#CustomArt_SetCustomBackground")), %a%.createElement(%b%.%c%',
                         'Object(%a%.%b%)("#CustomArt_',
                         'Object(%a%.%b%)([%c%.%d%], %e%.prototype, "OnChangeHero", null)']}},
             'library.js': {}}
        )
        
    def test_get_refs1(self):
        r_print(self.a.refs_data)
        
    def test_get_file_refs1(self):
        #self.a.get_refs_for_file("libraryroot.js", )
        pass
            
    def test_refs_in_tweak1(self):
        self.assertEqual(self.a.split_refs_sublist(['a','b']), ('a', ['b']))
        self.assertEqual(self.a.split_refs_sublist('a'), ('a', ''))
        print(self.a.split_refs_sublist([]))
        
    def sub_extras1(self):
        self.r.sub_extras_with_letters('Object(%a%.%b%)([%c%.%d%], %e%.prototype, "OnRemoveHero", null)', ('r', 'c', 'A', 'a', 't'))

class TestPopulateRefs(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.y = js_tweaker.YamlHandler(sys.path[0] + "/../js_tweaks.yml")
        cls.a = js_manager.ConfigJSHandler(cls.y.data, backend.load_config())
        cls.r = js_tweaker.RegexHandler()    
    
    def test_populate_refs1(self):
        self.a.populate_data_refs(self.a.search_for_refs())
        
    def test_convert_extras1(self):
        letters = ('r', 'c', 'A', 'a', 't')
        self.a.convert_extra_refs(['Object(%a%.%b%)([%c%.%d%], %e%.prototype, "OnRemoveHero", null)'],letters)
        print()
        
if __name__ == '__main__':
    #suite = unittest.TestLoader().loadTestsFromModule(sys.modules[__name__])
    #unittest.TextTestRunner(verbosity=3).run(suite)
    unittest.main(argv=['ignored', '-v', 'TestRefs.test_search_refs5'], exit=False)
    #unittest.main(argv=['ignored', '-v', 'TestRefs.test_get_refs1'], exit=False)
    #unittest.main(argv=['ignored', '-v', 'TestJSManager.test_full_process_yaml'], exit=False)
    #unittest.main(argv=['ignored', '-v', 'TestPopulateRefs.test_populate_refs1'], exit=False)
    #unittest.main(argv=['ignored', '-v', 'TestPopulateRefs.test_convert_extras1'], exit=False)
    #unittest.main(argv=['ignored', '-v', 'TestRefs.test_refs_in_tweak1'], exit=False)
    #unittest.main(argv=['ignored', '-v', 'TestRefs.sub_extras1'], exit=False)