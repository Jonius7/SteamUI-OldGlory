import unittest
import backend

#CSS Line Parser
class TestCSSLineParser(unittest.TestCase):

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
    '''
    def test_write_before_theme(self):
        backend.add_new_css_theme("shiina.css", "before", {"start" : "DO NOT EDIT THESE !!! DO NOT EDIT THESE",
                  "end" : "END steam-library tweaks for SteamUI-OldGlory"})

    def test_write_after_theme(self):
        backend.add_new_css_theme("acrylic.css", "after", {"start" : "DO NOT EDIT THESE !!! DO NOT EDIT THESE",
                  "end" : "END steam-library tweaks for SteamUI-OldGlory"})
        

if __name__ == '__main__':
    unittest.main()
