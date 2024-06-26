import unittest
import sys
from pathlib import Path
sys.path.append(str(Path('.').absolute().parent))
import backend
import time
import os


os.chdir("..")
#CSS Line Parser
class TestCSSLineParser(unittest.TestCase):
    #unittest.main(warnings='ignore')
    
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
    
    def test_write_before_theme(self):
        backend.add_new_css_theme("shiina.css", "before", {"start" : "DO NOT EDIT THESE !!! DO NOT EDIT THESE",
                  "end" : "END steam-library tweaks for SteamUI-OldGlory"})

    def test_write_after_theme(self):
        backend.add_new_css_theme("acrylic.css", "after", {"start" : "DO NOT EDIT THESE !!! DO NOT EDIT THESE",
                  "end" : "END steam-library tweaks for SteamUI-OldGlory"})
    
    def test_filename_too_long_for_html(self):
        self.assertRaises(Exception, backend.patch_html("aaaabbbbccccdddde.css"))
    '''

    #def test_get_json(self):
    #    backend.get_json_data()

    '''
    def test_get_function_performance(self):
        start_time = time.time()
        print(backend.get_git_file_hash("../scss/_sidebar.scss"))
        print("--- %s seconds ---" % (time.time() - start_time))

    
    def test_check_directory(self):
        j = backend.get_json_data()
        c = backend.check_new_commit_dates(j)        
        print(backend.hash_compare_small_update_files(c, j))
    '''
    
class TestThemeUpdater(unittest.TestCase):
    def test_theme_updater(self):
        tu = backend.ThemeUpdater("Jonius7", "SteamUI-OldGlory")
        tu.update_theme()
        print(tu.get_extracted_folder_name("Jonius7-SteamUI-OldGlory-234234"))
        tv = backend.ThemeUpdater("RoseTheFlower", "MetroSteam")
        tv.update_theme()
    
if __name__ == '__main__':
    unittest.main()
