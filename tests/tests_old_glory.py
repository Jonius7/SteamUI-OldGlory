import unittest

from pathlib import Path
import sys
sys.path.append(str(Path('.').absolute().parent))
import old_glory
import backend

#Test recursion for finding values in css_config
class TestApplyCssValues(unittest.TestCase):
    '''
    def test_one_level(self):
        self.assertEqual(
            old_glory.search("--WhatsNew", "Random", {"--WhatsNew" : "block"}),
            "block")

    def test_two_levels(self):
        self.assertEqual(
            old_glory.search("--WhatsNew", "Rag", {"What's New" : {"--WhatsNew" : "block"}}),
            "block")
       
    def test_full_default_config(self):
        self.assertEqual(
            old_glory.search("--WhatsNew", "Car", backend.CSS_CONFIG),
            "Car")
        
    def test_multiple_values(self):
        container = BlankClass("string")
        container.css_config = backend.CSS_CONFIG
        self.assertEqual(
            old_glory.apply_css_config_values(container, {"--WhatsNew" : "block", "--HoverOverlayPosition": "black"}),
            ["block", "black"])
    '''

    '''
    def test_simple_get_item(self):
        self.assertEqual(
            old_glory.get_item("--WhatsNew", {"--WhatsNew" : "block"}),
            "block")

    def test_full_get_item(self):
        print(old_glory.get_item("--WhatsNew", backend.CSS_CONFIG)["current"])
        self.assertEqual(
            old_glory.get_item("--WhatsNew", backend.CSS_CONFIG),
            "block")
    '''
    def test_css_config_reset(self):
        previous_value = backend.CSS_CONFIG["Left Sidebar - Games List"]["--HoverOverlayPosition"]["current"]
        self.assertEqual(
            "0",
            old_glory.css_config_reset(backend.CSS_CONFIG)["Left Sidebar - Games List"]["--HoverOverlayPosition"]["current"])

    def test_css_config_js(self):
        previous_value = backend.CSS_CONFIG["Left Sidebar - Games List"]["--HoverOverlayPosition"]["current"]
        self.assertEqual(
            "unset",
            old_glory.css_config_js_enabled(backend.CSS_CONFIG)["Left Sidebar - Games List"]["--HoverOverlayPosition"]["current"])

        
class BlankClass(object):
    def __init__(self, string):
        self.string = string


if __name__ == '__main__':
    unittest.main()