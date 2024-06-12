import unittest
from unittest.mock import mock_open, patch
import os
import sys
from pathlib import Path
#sys.path.append(str(Path('.').absolute().parent))
import backend
import js_tweaker
import datetime
import re
import shutil
from timeit import timeit
from rich import print as r_print

#CSS Line Parser
class TestCopyFilesFromSteam(unittest.TestCase):

    #def test_reset1(self):
    #    js_tweaker.copy_files_from_steam(reset=1)
    
    '''
    def test_withdefault(self):
        self.assertEqual(
            backend.css_line_parser("  --WhatsNew: ace;  /* Default: block. Set to none to hide What's New */"),
            {"name" : "--WhatsNew",
             "default" : "block",
             "current" : "ace",
             "desc" : "Set to none to hide What's New"})
        
    def test_nodefault(self):
        self.assertEqual(
            backend.css_line_parser("  --WhatsNew: ace;  /* DSet to none to hide What's New */"),
            {"name" : "--WhatsNew",
             "default" : "ace",
             "current" : "ace",
             "desc" : "DSet to none to hide What's New"})
        
    def test_nodefault_noendcomment(self):
        self.assertEqual(
            backend.css_line_parser("  --WhatsNew: ace;  /* DSet to none to hide What's New"),
            {"name" : "--WhatsNew",
             "default" : "ace",
             "current" : "ace",
             "desc" : "DSet to none to hide What's New"})
        
    def test_nodefault_nostartcomment(self):
        self.assertEqual(
            backend.css_line_parser("  --WhatsNew: ace;   DSet to none to hide What's New */"),
            None)

    def test_comments_nospaces(self):
        self.assertEqual(
            backend.css_line_parser("  --WhatsNew:ace; /*DSet to none to hide What's New*/"),
            {"name" : "--WhatsNew",
             "default" : "ace",
             "current" : "ace",
             "desc" : "DSet to none to hide What's New"})
    '''

    '''
    def test_run_fixes_modify(self):
        a, b = backend.load_js_fixes()
        backend.write_js_fixes(a, b)

    def test_find_fixes_variables(self):
        js_tweaker.find_fix_with_variable("$^: $^ * $^", "\\1: (\\3 - 10) * $^")

    def test_beaut_filename(self):
        print(js_tweaker.get_beaut_filename("libraryroot.js"))
        print(js_tweaker.get_beaut_filename("library.js"))

    def create_beaut_file(self):
        print(js_tweaker.beautify_js("libraryroot.js"))
        print(js_tweaker.beautify_js("library.js"))
    '''
    
class TestYaml(unittest.TestCase):
    ###
    def test_parse_yaml(self):
        yaml = js_tweaker.YamlHandler(os.path.join(sys.path[0], "js_tweaks.yml"))
        #print(yaml.data)
        r_print(yaml.data)

    '''def test_retrieve_find(self):
        yaml = self.test_parse_yaml()
        start_time = datetime.datetime.now()
        for fix in yaml.data:
            for find in yaml.data[fix]["strings"]:
                    #print(find)
                    pass
        end_time = datetime.datetime.now()
        print(end_time - start_time)

    def test_parse_old_fixes(self):
        start_time = datetime.datetime.now()
        js_tweaker.parse_fixes_file('../fixes.txt')
        end_time = datetime.datetime.now()
        print(end_time - start_time)'''

    #def test_write_modif(self):
    #    yaml = self.test_parse_yaml()
    #    js_tweaker.write_modif_file(yaml.data)   

'''class TestRegex(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ac = js_tweaker.RegexHandler()
    
    def test_semantic_1(self):
        print(js_tweaker.semantic_find_str('onContextMenu: this.OnContextMenu,~~hoverDelay: 300,'))

    def test_semantic_2(self):
        print(js_tweaker.semantic_find_str('onContextMenu: this.OnContextMenu,hoverDelay: 300,'))

    def test_regex_cap_groups(self):
        print(re.sub('\\\\([0-9])+', '\\(\\1)', 'Object\\(\\\\1\\.\\\\2\\)\\(\\[\\\\3\\.\\\\4\\]'))


    def test_sub_vars(self):
        print(self.ac.sub_find_with_regex("Object(%1%.%1%)([%2%, %3%], %4%)"))

    def test_combined_regex1(self):
        bb = self.ac.sub_find_with_regex('.apply(console, Object(%1%.%2%)([%3%, %4%], %5%))')
        bc = self.ac.sub_repl_with_regex('.apply(console, Object(%1%.%2%)([%3%, %4%], %5%))*/')

        print(js_tweaker.unescape(re.sub(bb, bc, '.apply(console, Object(p.g)([e, t], n))')))

    def test_combined_regex2(self):
        #start_time = datetime.datetime.now()
        bb = self.ac.sub_find_with_regex('y: %1% * %2%')
        bc = self.ac.sub_repl_with_regex('y: %1% * (%2% - 10)')

        print(js_tweaker.unescape(re.sub(bb, bc, 'y: dd * ac')))
        #end_time = datetime.datetime.now()
        #print(end_time - start_time)

    def test_combined_regex_func1(self):
        #start_time = datetime.datetime.now()
        cd = 'Object(%1%.%2%)([%3%.%4%], e.prototype, "OnChangeHero", null),'
        ce = 'Object(%1%.%2%)([%3%.%4%], e.prototype, "OnChangeHero", null), Object(%1%.%2%)([%3%.%4%], e.prototype, "OnRemoveHero", null),'

        #print(self.ac.find_and_repl(cd, ce, 'Object(a.c)([E.a], e.prototype, "OnChangeHero", null),'))
        #end_time = datetime.datetime.now()
        #print(end_time - start_time)

    def test_combined_regex_func2(self):
        #start_time = datetime.datetime.now()
        cd = 'Object(%1%.%2%)([%3%.%4%], e.prototype, "OnChangeHero", null),'
        ce = 'Object(%1%.%2%)([%3%.%4%], e.prototype, "OnChangeHero", null), Object(%1%.%2%)([%3%.%4%], e.prototype, "OnRemoveHero", null),'

        print("PROTO")
        print(self.ac.find("gesgas", 'segesgesgasegase'))
        #end_time = datetime.datetime.now()
        #print(end_time - start_time)

    def test_semantic(self):
        print(js_tweaker.semantic_find_str('switch (t) {~~case 38:'))

'''

if __name__ == '__main__':
    unittest.main()
