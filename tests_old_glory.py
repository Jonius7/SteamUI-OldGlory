import unittest
import old_glory
import backend

#Test recursion for finding values in css_config
class TestApplyCssValues(unittest.TestCase):
    
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


class BlankClass(object):
    def __init__(self, string):
        self.string = string


if __name__ == '__main__':
    unittest.main()
