import unittest

from pathlib import Path
import sys
sys.path.append(str(Path('.').absolute().parent))
import old_glory
import backend
import tkinter as tk
import os
import datetime

#Test recursion for finding values in css_config
class TestApplyCssValues(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dummyController = old_glory.OldGloryApp()
        cls.dummyFrame = tk.Frame(cls.dummyController)
        cls.dummyController.json_data = backend.get_json_data(sys.path[0] + '/../old_glory_data.json')
        cls.dummyController.oldglory_config = backend.load_config(sys.path[0] + '/../oldglory_config2.cfg')
    
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
    

    def test_getpresetoptions(self):
        dummyController = old_glory.OldGloryApp()
        dummyFrame = tk.Frame(dummyController)
        json_data = backend.get_json_data()
        presetFrame = tk.Frame(dummyFrame)
        x = old_glory.PresetFrame(dummyFrame, dummyController, json_data)
        presetFrame = x.returnPresetFrame()
        presetFrame.pack()

        dummyFrame.pack()

        x.getPresetOptions()
    '''

    def add_dummy_frame(self):
        json_data = backend.get_json_data()
        presetFrame = tk.Frame(self.dummyFrame)
        pFrame = old_glory.PresetFrame(self.dummyFrame, self.dummyController, json_data)
        presetFrame = pFrame.returnPresetFrame()
        presetFrame.pack()

        self.dummyFrame.pack()

        return self.dummyController
   
    def test_showpresetoptions(self):
        x = self.add_dummy_frame()
        print(type(x.json_data))

    
    '''
    def test_updatewindow(self):
        dummyController = old_glory.OldGloryApp()
        dummyUpdate = old_glory.UpdateWindow(
            controller=self,
            file_dates=backend.check_new_commit_dates(dummyController.json_data))
    '''

    def test_is_connected(self):
        old_glory.is_connected()

    def test_open(self):
        backend.OS_open_file(os.getcwd())

    def test_check_disabled(self):
        x = self.add_dummy_frame()
        x.frames["StartPage"].check1.event_generate("<Button-1>")
        print(x.frames["StartPage"].check2.cget("state"))

    def test_get_libraryroot(self):
        print("LIBRARYROOT FILENAME: " + self.dummyController.get_libraryroot_filename())

    def test_get_patcher(self):
        print("PATCHER PATH: " + self.dummyController.get_patcher_path())
    
     
    '''def test_run_js_tweaker(self):
        #/start_time = datetime.datetime.now()
        old_glory.run_js_tweaker(self.dummyController.frames["StartPage"].text1)
        #end_time = datetime.datetime.now()
        #print(end_time - start_time)'''
    
        
class BlankClass(object):
    def __init__(self, string):
        self.string = string




if __name__ == '__main__':
    #suite = unittest.TestLoader().loadTestsFromModule(sys.modules[__name__])
    #unittest.TextTestRunner(verbosity=3).run(suite)
    #unittest.main(argv=['ignored', '-v', 'TestApplyCssValues.test_run_js_tweaker'], exit=False)
