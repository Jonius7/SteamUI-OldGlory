import sys
import asyncio
import time
import queue
import urllib.error

'''
from PIL import ImageTk, Image

import platform
import traceback
import requests
import webbrowser
import socket
from functools import partial
#import re
'''
from threading import Thread, Event


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
              "EnableVerticalNavBar" : {"value" : "var3", "check" : "check3", "javascript" : False},
              "EnableClassicLayout" : {"value" : "var4", "check" : "check4", "javascript" : False},
              "LandscapeImages" : {"value" : "var5", "check" : "check5", "javascript" : True},
              #"InstallWithDarkLibrary" : {"value" : "var6", "javascript" : False},
              "InstallWithLibraryTheme" : {"value" : "var6", "check" : "check6", "javascript" : False},
              "ClassicStyling" : {"value" : "var7", "check" : "check7", "javascript" : False},
              "HomeButton" : {"value" : "var8", "check" : "check8", "javascript" : False},
              "ThemeSelected" : {"set" : ""}
              }

### INSTALL Functions
### ================================

def worker0a(q: queue.Queue, event: Event, controller):
    q.put(backend.steam_running())
    event.set()
    
def worker0b(q: queue.Queue, event: Event, result_container):
    event.wait()
    try:
        result = q.get()
        result_container.append(result)
    except queue.Empty:
        print("Queue is empty, could not get the result.")

def worker1a(q: queue.Queue, event: Event, controller):
    try:
        print("Refreshing Steam window...")
        #q.put_nowait(backend.request_url())
        q.put(backend.request_url())
        event.set()
    except urllib.error.URLError:
        print("Is Steam running? Unable to refresh Steam window (requires SFP/Millennium) \n\
            Alternatively run Steam with the -cef-enable-debugging argument", file=sys.stderr)
    except:
        print("Unable to refresh Steam window", file=sys.stderr)
        backend.print_traceback()
    finally:
        enable_buttons_after_installing(controller)
        
def worker1b(q: queue.Queue, event: Event):
    event.wait()
    result = q.get()
    asyncio.run(backend.refresh_steam(result))
    #print(f"Second thread received: {result}")
    print("Steam window refreshed.")

def threads_setup_refresh_steam(controller):
    result_container = []
    q0 = queue.Queue()
    event0 = Event()
    exists1_thread = Thread(target = worker0a, args = (q0, event0, controller))
    exists1_thread.start()
    exists2_thread = Thread(target = worker0b, args = (q0, event0, result_container))
    exists2_thread.start()
    
    while not event0.is_set():
        time.sleep(0.01)
        
    if result_container:
        final_result = result_container[0]
        #print(f"Final result: {final_result}")
    else:
        final_result = None
    
    if final_result:
        q1 = queue.Queue()
        event1 = Event()
        url_thread = Thread(target = worker1a, args = (q1, event1, controller))
        url_thread.start()
        return {"result": final_result, 
                "queue": q1,
                "event": event1}
    else:
        return {"result": final_result}
    
def threads_execute_refresh_steam(thread_data, controller):
    if thread_data["result"]:
        #thread2 = ThreadWithCallback(target = worker1b, args = (thread_data["queue"], thread_data["event"]),
        #                                    callback = lambda: enable_buttons_after_installing(controller))
        thread2 = Thread(target = worker1b, args = (thread_data["queue"], thread_data["event"]))
        thread2.start()
        return thread2

def install_click(event, page, controller):
    if str(event.widget['state']) == 'normal':
        try:
            disable_buttons_while_installing(controller)
            
            '''result_container = []
            q0 = queue.Queue()
            event0 = Event()
            exists1_thread = Thread(target = worker0a, args = (q0, event0))
            exists1_thread.start()
            exists2_thread = Thread(target = worker0b, args = (q0, event0, result_container))
            exists2_thread.start()
            
            while not event0.is_set():
                time.sleep(0.01)
            
            if result_container:
                final_result = result_container[0]
                #print(f"Final result: {final_result}")
            
            if final_result:
                q1 = queue.Queue()
                event1 = Event()
                url_thread = Thread(target = worker1a, args = (q1, event1, controller))
                url_thread.start()
            '''

            thread_in_progress_data = threads_setup_refresh_steam(controller)
            
            settings = get_settings_from_gui(page)
            set_filepaths_config(page, controller)
            settings = set_js_config(controller, settings)
            apply_special_js_config(controller)
            #print(settings)
            #print(page.loaded_config)
            
            ### To be changed in a later version
            backend.write_js_fixes(controller.js_config, controller.special_js_config)
            backend.write_css_configurables(controller.css_config)
            backend.update_steamui_websrc_hash(controller.json_data)
            
            #applying settings
            change_javascript = check_if_css_requires_javascript(page, controller, settings)
            if controller.mode_changed == 1:
                change_javascript = page.ConfirmObject.install_modes.index(
                    page.ConfirmObject.modeVar.get()
                )
            #print(page.ConfirmObject.modeVar.get())
            set_mode_menu_var(controller, change_javascript)
            manager_write_css_settings(page, controller, settings)
            thread = manager_run_js_tweaker(page, controller, change_javascript)
            
            update_loaded_config(page, controller)
            loaded_config_to_oldglory_dict(controller)
            backend.write_config(controller.oldglory_config)
            
            apply_css_theme(controller.frames["StartPage"], controller)
            backend.compile_css(backend.get_json_data())
            controller.js_gui_changed = 0
            controller.mode_changed = 0
            backend.backup_libraryroot_css(controller.oldglory_config["Filepaths"]["InstallMode"])
            
            update_loaded_config(page, controller)
            
            if thread_in_progress_data["result"]:
                second_thread = threads_execute_refresh_steam(thread_in_progress_data, controller)
                if not second_thread:
                    enable_buttons_after_installing(controller)
            elif not thread:
                enable_buttons_after_installing(controller)
            
            # Will be removed once refresh_steam is working in exe
            #backend.refresh_steam_dir()
            #while True:
            #    if not url_thread.is_alive():
            #        break
            #    thread2 = Thread(target = asyncio.run, args = (backend.refresh_steam(socket_url),))
            #    thread2.start()
            
            
            
        except:
            print("Error while installing tweaks.", file=sys.stderr)
            old_glory.print_traceback()
            enable_buttons_after_installing(controller)
    
def disable_buttons_while_installing(controller):
    for frame in controller.frames:
        controller.frames[frame].ConfirmObject.disable_install_button()

def enable_buttons_after_installing(controller):
    for frame in controller.frames:
        controller.frames[frame].ConfirmObject.enable_install_button()
        
def mode_click(event, controller):
    #print(str(event.widget['state']))
    controller.mode_changed = 1
    pass


def get_settings_from_gui(page, config_map=CONFIG_MAP):
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

def set_filepaths_config(page, controller):
    try:
        #print(controller.oldglory_config)
        controller.oldglory_config["Filepaths"]["InstallMode"] = page.dropdown5.get()
    except:
        print("Error while setting filepaths config (includes install location).", file=sys.stderr)
        old_glory.print_traceback()

def set_js_config(controller, settings):
    SETTINGS_MAP = {
        "LandscapeImages": {"JS_name" : "Landscape Images JS Tweaks"}
    }
    #print(settings)
    #print(controller.js_config)
    for setting in SETTINGS_MAP:
        for curr_setting, curr_value in controller.js_config.items():
            if SETTINGS_MAP[setting]["JS_name"] in curr_setting:
                js_name = curr_setting
                #print(js_name)
                controller.js_config[js_name] = str(settings[setting]["value"])
                controller.frames["JSPage"].js_gui.checkvars[js_name].set(settings[setting]["value"])
    return settings

def apply_special_js_config(controller):       
    for key in controller.special_js_config:
        if "Change Game Image Grid Sizes" in key:
            sizes = ["Small", "Medium", "Large"]
            for size in sizes:
                controller.special_js_config[key][size] = controller.frames["JSPage"].js_gui.comboboxes[size].get()

def check_if_css_requires_javascript(page, controller, settings):
    change_javascript = 0   #Check if js required
    for setting in settings:
        if check_setting_requires_javascript(settings[setting]):
            if setting in page.loaded_config \
                and int(page.loaded_config[setting]) != int(settings[setting]["value"]): #If Setting is different
                    #set_css_config_js_enabled(controller.css_config)
                    change_javascript = 1
    if controller.js_gui_changed == 1:
        #set_css_config_js_enabled(controller.css_config)
        change_javascript = 1
    return change_javascript

def set_mode_menu_var(controller, change_javascript):
    if change_javascript == 1 or change_javascript == 0:
        for page in controller.frames:
            controller.frames[page].ConfirmObject.set_mode_menu(change_javascript)  
        #print(change_javascript)      

def check_setting_requires_javascript(setting_data):
    if "javascript" in setting_data and setting_data["javascript"]:
        return True
    else:
        return False

def manager_write_css_settings(page, controller, settings):    
    # Write to libraryroot.custom.scss
    page.text1.update_idletasks()
    
    backend.write_css_sections(controller.sections_config, 
                               backend.read_css_sections(), 
                               controller.json_data["sections"])
    page.text1.update_idletasks()
    
    backend.write_css_settings(settings)
    page.text1.update_idletasks()
    print("Applied CSS Settings.")    
    
def manager_run_js_tweaker(page, controller, change_javascript):     
    ### Run js_tweaker if required
    if change_javascript == 1:
        #failed implementation due to needing controller state for each page with Install button
        #page.ConfirmObject.disable_install_button()
        thread = ThreadWithCallback(target = old_glory.run_js_tweaker, args = (controller,),
                                    callback = lambda: enable_buttons_after_installing(controller))
        thread.start() 
    else:
        thread = False;
    return thread;
    

class ThreadWithCallback(Thread):
    def __init__(self, *args, **kwargs):
        self.callback = kwargs.pop("callback")
        super(ThreadWithCallback, self).__init__(*args, **kwargs)
    def run(self, *args, **kwargs):
        super(ThreadWithCallback, self).run(*args, **kwargs)
        #print(self.callback)
        self.callback()

#update loaded_config on Install click
def update_loaded_config(page, controller):
    for key in page.loaded_config:
        if "value" in CONFIG_MAP[key]:
            page.loaded_config[key] = str(page.getCheckbuttonVal(CONFIG_MAP[key]["value"]).get())
        elif "set" in CONFIG_MAP[key]:
            if key == "ThemeSelected":
                theme_full_name = page.dropdown6.get()
                theme_name = theme_full_name.split(" (")[0]
                page.loaded_config[key] = theme_name
                #settings_values[key] = page.dropdown6.get().split(" (")[0]
            #else:
                #settings_values[key] = CONFIG_MAP[key]["set"]

    
def loaded_config_to_oldglory_dict(controller, section="Main_Settings"):
    #print(controller.oldglory_config)
    #print("===")
    #print(controller.frames["StartPage"].loaded_config)
    
    oldglory_config = controller.oldglory_config
    loaded_config = controller.frames["StartPage"].loaded_config
    
    for setting in loaded_config:
        if setting in oldglory_config[section]:
            oldglory_config[section][setting] = loaded_config[setting]
    #print(oldglory_config)

#need rewrite
def apply_css_theme(page, controller):
    if page.var6.get() == 1:
        theme_full_name = page.dropdown6.get()
        print("Applying CSS Theme: " + theme_full_name)
        theme_name = theme_full_name.split(" (")[0]
        #print(controller.json_data["themes"][theme_name]["filename"])
        backend.enable_css_theme(theme_name,
                         controller.json_data["themes"][theme_name]["order"],
                         controller.json_data)
    elif page.var6.get() == 0 and page.change_theme == 1:
        backend.enable_css_theme("name", "after", controller.json_data)
    page.change_theme = 0


### StartPage
### Select checkboxes based on config
def set_selected_main_options(page, controller):
    try:
        ### grab stdout, stderr from function in backend
        #f = io.StringIO()
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
                        print("Could not auto-select current theme: " + loaded_config[key], file=sys.stderr)
                    #page.getDropdownVal("dropdown6").set(loaded_config[key])
        return loaded_config
    except Exception as e:
        print(e, file=sys.stderr)
        
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