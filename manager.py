import tkinter as tk
import tkinter.font as TkFont
from tkinter import ttk
import io
import os
import sys
'''
from PIL import ImageTk, Image

import platform
import traceback
import requests
import webbrowser
import socket
from functools import partial
#import re
from threading import Thread
'''

import old_glory
import backend
import js_tweaker
#import custom_tk


### Map config values to selected checkboxes
CONFIG_MAP = {"SteamLibraryPath" : {"set" : ""},
              "PatcherPath" : {"set" : ""},
              "" : {},
              "InstallCSSTweaks" : {"value" : "var1", "check" : "check1", "javascript" : False},
              "EnablePlayButtonBox" : {"value" : "var2", "check" : "check2", "javascript" : False},
              "EnableVerticalNavBar" : {"value" : "var3", "check" : "check3", "javascript" : True},
              "EnableClassicLayout" : {"value" : "var4", "check" : "check4", "javascript" : True},
              "LandscapeImages" : {"value" : "var5", "check" : "check5", "javascript" : True},
              #"InstallWithDarkLibrary" : {"value" : "var6", "javascript" : False},
              "InstallWithLibraryTheme" : {"value" : "var6", "check" : "check6", "javascript" : False},
              "ClassicStyling" : {"value" : "var7", "check" : "check7", "javascript" : False},
              "ThemeSelected" : {"set" : ""}
              }

### INSTALL Functions
### ================================

### Install Click
def install_click_OLD(event, page, controller):
    try:
        print("==============================")
        #get settings
        settings_to_apply, settings_values = get_settings_from_gui(event, page)

        #make any js_config enable/disable required based on main options
        settings_values = apply_changes_to_config(controller, settings_values)
        
        #write fixes.txt before apply
        backend.write_js_fixes(controller.js_config, controller.special_js_config)

        #write css configurables
        backend.write_css_configurables(controller.css_config)

        #applying settings
        apply_settings_from_gui(page, controller, settings_to_apply, settings_values)
        backend.write_config(settings_values)

        #add/remove theme
        apply_css_theme(controller.frames[StartPage], controller)

        #enable/disable modules (TODO)

        #compile css from scss
        #print(controller.json_data)
        #backend.compile_css(controller.json_data)
        backend.compile_css(backend.get_json_data())
        
        #reset state of js gui to "unchanged"
        controller.js_gui_changed = 0
        backend.refresh_steam_dir()
        update_loaded_config(page, controller)
    except:
        print("Error while installing tweaks.", file=sys.stderr)
        print_traceback()

def install_click(event, page, controller):
    get_settings_from_gui(event, page)
    #print("===")
    #print(controller.js_gui_changed)
        
### Get settings to apply (with validation), and values

def get_settings_from_gui(event, page, config_map = CONFIG_MAP):
    try:
        settings = {}
        for key in config_map:
            if "value" in config_map[key]:
                settings[key] = {"value" : str(page.getCheckbuttonVal(config_map[key]["value"]).get()),
                                 "state" : str(page.getCheck(config_map[key]["check"]).cget('state')),
                                 "javascript" : config_map[key]["javascript"]}
                
                print(settings[key])            
        
        
    except:
        print("Error while installing tweaks.", file=sys.stderr)
        old_glory.print_traceback()


### some of this needs to be changed to account for "unchecking" options
def get_settings_from_gui_OLD(event, page):
    try:
        settings = []
        settings_values = {}
        for key in CONFIG_MAP:
            if "value" in CONFIG_MAP[key]:
                check_button_val = page.getCheckbuttonVal(CONFIG_MAP[key]["value"]).get()         
                settings_values[key] = check_button_val
                if check_button_val == 1:
                    settings.append(key)
                elif check_button_val != int(page.loaded_config[key]):
                    #print("BOX UNSELECTED")
                    settings.append(key)
            elif "set" in CONFIG_MAP[key]:
                if key == "ThemeSelected":
                    settings_values[key] = page.dropdown6.get().split(" (")[0]
                else:
                    settings_values[key] = CONFIG_MAP[key]["set"]    
            else:
                settings_values[""] = ""
        #print("ARRAY ")
        settings_to_apply = backend.validate_settings(settings)
        #print(settings_to_apply)
        #print(settings_values)
        return settings_to_apply, settings_values
        
    except FileNotFoundError:
        print("Error: Unable to get settings from checkboxes.", file=sys.stderr)
        print_traceback()
### v1

### StartPage
### Select checkboxes based on config
def set_selected_main_options(page, controller):
    try:
        ### grab stdout, stderr from function in backend
        f = io.StringIO()
        #loaded_config = backend.load_config()
        loaded_config = controller.oldglory_config["Main_Settings"]
        for key in loaded_config:
            if key in CONFIG_MAP:
                if loaded_config[key] == '0' :
                    page.getCheckbuttonVal(CONFIG_MAP[key]["value"]).set(0)
                elif loaded_config[key] == '1' :
                    page.getCheckbuttonVal(CONFIG_MAP[key]["value"]).set(1)
                elif key == "ThemeSelected":
                    #print(loaded_config[key])
                    try:
                        theme_entry = controller.json_data["themes"][loaded_config[key]]
                        if (theme_entry):
                            #could be fragile but otherwise works
                            page.getDropdownVal("dropdown6").set(loaded_config[key] + " (" + theme_entry["author"] + ")")
                    except:
                        print("Could not auto-select current theme.", file=sys.stderr)
                    #page.getDropdownVal("dropdown6").set(loaded_config[key])
        return loaded_config
    except Exception as e:
        print(e.message, file=sys.stderr)
        
### ================================