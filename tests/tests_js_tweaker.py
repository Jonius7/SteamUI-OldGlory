import unittest
import sys
from pathlib import Path
sys.path.append(str(Path('.').absolute().parent))
import backend
import js_tweaker
import datetime

#CSS Line Parser
class TestCopyFilesFromSteam(unittest.TestCase):

    def test_reset1(self):
        js_tweaker.copy_files_from_steam(reset=1)
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

    def test_run_fixes_modify(self):
        a, b = backend.load_js_fixes()
        backend.write_js_fixes(a, b)

    def test_find_fixes_variables(self):
        js_tweaker.find_fix_with_variable("$^: $^ * $^", "\\1: (\\3 - 10) * $^")

    def test_parse_yaml(self):
        #yaml = js_tweaker.YamlHandler.parse_yaml_file(sys.path[0] + "/../js_tweaks.yml")
        yaml = js_tweaker.YamlHandler(sys.path[0] + "/../js_tweaks.yml")
        return yaml

    def test_retrieve_find(self):
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
        js_tweaker.parse_fixes_file('fixes.txt')
        end_time = datetime.datetime.now()
        print(end_time - start_time)

    def test_write_modif(self):
        yaml = self.test_parse_yaml()
        js_tweaker.write_modif_file(yaml.data)

    def test_semantic_1(self):
        print(js_tweaker.semantic_find_str('onContextMenu: this.OnContextMenu,~~hoverDelay: 300,'))

    def test_semantic_2(self):
        print(js_tweaker.semantic_find_str('onContextMenu: this.OnContextMenu,hoverDelay: 300,'))
        
if __name__ == '__main__':
    unittest.main()
