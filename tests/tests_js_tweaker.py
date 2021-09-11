import unittest
import sys
from pathlib import Path
sys.path.append(str(Path('.').absolute().parent))
import backend
import js_tweaker

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

if __name__ == '__main__':
    unittest.main()
