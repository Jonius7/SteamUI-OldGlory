import unittest

from pathlib import Path
import sys
sys.path.append(str(Path('.').absolute().parent))
import old_glory
import manager
import backend
import tkinter as tk
import os

#Test recursion for finding values in css_config
class TestCheckManager(unittest.TestCase):

    def setUp(self):
        self.dummyController = old_glory.OldGloryApp()
    
    def add_dummy_frame(self):
        dummyFrame = tk.Frame(dummyController)
        json_data = backend.get_json_data()
        presetFrame = tk.Frame(dummyFrame)
        pFrame = old_glory.PresetFrame(dummyFrame, dummyController, json_data)
        presetFrame = pFrame.returnPresetFrame()
        presetFrame.pack()

        dummyFrame.pack()

        return dummyController
    
    def test_get_settings_from_gui(self):
        settings = manager.get_settings_from_gui(self.dummyController.frames["StartPage"])
        backend.write_css_settings(settings)

    def test_check_loaded(self):
        #dummyController = self.create()
        print(manager.loaded_config_to_oldglory_dict(self.dummyController))
        
if __name__ == '__main__':
    unittest.main()
