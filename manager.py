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
CONFIG_MAP = {#"SteamLibraryPath" : {"set" : ""},
              #"PatcherPath" : {"set" : ""},
              #"" : {},
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
    settings = get_settings_from_gui(event, page)
    #settings = apply_changes_to_config(controller, settings)
    settings = set_js_config(controller, settings)
    apply_special_js_config(controller)
    print(settings)
    print(page.loaded_config)
    
    ### To be changed in a later version
    #write fixes.txt before apply
    backend.write_js_fixes(controller.js_config, controller.special_js_config)
    #write css configurables
    backend.write_css_configurables(controller.css_config)
    ###
    
    #applying settings
    apply_settings_from_gui(page, controller, settings)
    #backend.write_config(settings_values)
    
        
def get_settings_from_gui(event, page, config_map=CONFIG_MAP):
    '''
    Returns a dictionary of settings to apply ("value", "state", "javascript")
    '''
    try:
        settings = {}
        for key in config_map:
            if "value" in config_map[key]:
                settings[key] = {"value" : str(page.getCheckbuttonVal(config_map[key]["value"]).get()),
                                 "state" : str(page.getCheck(config_map[key]["check"]).cget('state')),
                                 "javascript" : config_map[key]["javascript"]}
                
                #print(key + " | ", end="")
                #print(settings[key])
            if key == "ThemeSelected":
                    settings[key] = page.dropdown6.get().split(" (")[0]
        return settings      
        
        
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


def set_js_config(controller, settings):
    SETTINGS_MAP = {
        "EnableVerticalNavBar": {"JS_name" : "Vertical Nav Bar (beta, working)"},
        "LandscapeImages": {"JS_name" : "Landscape Images JS Tweaks (beta, working, some layout quirks with shelves)"}
    }
    for setting in SETTINGS_MAP:
        if setting in settings:
            js_name = SETTINGS_MAP[setting]["JS_name"]
            controller.js_config[js_name] = str(settings[setting]["value"])
            controller.frames["PageTwo"].js_gui.checkvars[js_name].set(settings[setting]["value"])
    return settings

def apply_special_js_config(controller):       
    for key in controller.special_js_config:
        if "Change Game Image Grid Sizes" in key:
            sizes = ["Small", "Medium", "Large"]
            for size in sizes:
                controller.special_js_config[key][size] = controller.frames["PageTwo"].js_gui.comboboxes[size].get()
    
# Rather not have this as hard coded as it currently is
def apply_changes_to_config_OLD(controller, settings_values):
    #print(settings_values.keys())
    if "EnableVerticalNavBar" in settings_values.keys():
        controller.js_config["Vertical Nav Bar (beta, working)"] = str(settings_values["EnableVerticalNavBar"])
        controller.frames["PageTwo"].js_gui.checkvars["Vertical Nav Bar (beta, working)"].set(settings_values["EnableVerticalNavBar"])
    if "EnableClassicLayout" in settings_values.keys():
        if settings_values["EnableClassicLayout"] == 1 and settings_values["EnableVerticalNavBar"] == 0:
            settings_values["EnableClassicLayout"] = 0        
    if "LandscapeImages" in settings_values.keys():
        controller.js_config["Landscape Images JS Tweaks (beta, working, some layout quirks with shelves)"] = str(settings_values["LandscapeImages"])
        controller.frames["PageTwo"].js_gui.checkvars["Landscape Images JS Tweaks (beta, working, some layout quirks with shelves)"].set(settings_values["LandscapeImages"])
    for key in controller.special_js_config:
        if "Change Game Image Grid Sizes" in key:
            sizes = ["Small", "Medium", "Large"]
            for size in sizes:
                controller.special_js_config[key][size] = controller.frames["PageTwo"].js_gui.comboboxes[size].get()
    return settings_values
    #print(controller.special_js_config)

### Write CSS settings (comment out sections) + run js_tweaker if needed
def apply_settings_from_gui_OLD(page, controller, settings_to_apply, settings_values):

    ### Check if js required
    change_javascript = 0
    for setting in settings_values:
        #print("javascript" in CONFIG_MAP[setting])
        if "javascript" in CONFIG_MAP[setting]:
            if CONFIG_MAP[setting]["javascript"] \
            and int(page.loaded_config[setting]) != page.getCheckbuttonVal(CONFIG_MAP[setting]["value"]).get():
                #print(int(page.loaded_config[setting]))
                #print(page.getCheckbuttonVal(CONFIG_MAP[setting]["value"]).get())
                set_css_config_js_enabled(controller.css_config)
                change_javascript = 1
    if controller.js_gui_changed == 1:
        set_css_config_js_enabled(controller.css_config)
        change_javascript = 1

    # Write to libraryroot.custom.css
    print("Applying CSS settings...")
    page.text1.update_idletasks()
    backend.write_css_settings(settings_to_apply, settings_values, controller.css_config)
    page.text1.update_idletasks()
    
    ### Run js_tweaker if required

    if change_javascript == 1:
        thread = Thread(target = run_js_tweaker, args = (page.text1, ))
        thread.start()
        #thread.join()
        #run_js_tweaker(page.text1)
        
    print("Settings applied.")


def apply_settings_from_gui(page, controller, settings):
    change_javascript = 0   #Check if js required
    for setting in settings:
        if check_setting_requires_javascript(settings[setting]):
            if setting in page.loaded_config \
                and int(page.loaded_config[setting]) != int(settings[setting]["value"]):
                    set_css_config_js_enabled(controller.css_config)
                    change_javascript = 1
    if controller.js_gui_changed == 1:
        set_css_config_js_enabled(controller.css_config)
        change_javascript = 1
    print(change_javascript)

def check_setting_requires_javascript(setting_data):
    if "javascript" in setting_data and setting_data["javascript"]:
        return True
    else:
        return False

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

### Set some CSS values back to "default"
### ================================
### Mainly HoverPosition
def set_css_config_no_js(css_config):
    css_config["Left Sidebar - Games List"]["--HoverOverlayPosition"]["current"] = "0"
    return css_config

def set_css_config_js_enabled(css_config):
    css_config["Left Sidebar - Games List"]["--HoverOverlayPosition"]["current"] = "unset"
    return css_config