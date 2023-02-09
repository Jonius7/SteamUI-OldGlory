import tkinter as tk
import tkinter.font as TkFont
from tkinter import ttk
from PIL import ImageTk, Image
import sys
import io
import os
import platform
import traceback
import requests
import webbrowser
import socket
from functools import partial
#import re
from threading import Thread

import manager
import backend
import js_tweaker
import custom_tk


OS_TYPE = platform.system()
DEBUG_STDOUT_STDERR = False # Only useful for debugging purposes, set to True

class OldGloryApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        self.version = "v0.9.27.12"
        self.release = "5.10.7"
      
        ### Window Frame
        tk.Tk.__init__(self, *args, **kwargs)
        self.container = tk.Frame(self)
        
        ### Data and Config (will be populated)
        self.json_data = None
        self.css_config = None
        self.js_config = None

        ### Fixed DPI Scaling on Windows
        if OS_TYPE == "Windows":
            #dpi = window.winfo_fpixels('1i')
            self.call('tk', 'scaling', 1.3)

        ### Window Dimensions/Position (width, height)
        self.set_window_dimensions(760, 660)

        ### Icon and Title
        add_window_icon(self)
        self.wm_title("SteamUI-OldGlory Installer " + self.release)
        
        ### Custom tk Styling
        self.set_tk_styles()

        ### Grid configure
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        ### Load config variables
        self.js_gui_changed = 0
        
        ### Frames/Pages configure
        self.frames = {}
        
        for F in (StartPage, CSSPage, JSPage):
            frame = F(self.container, self)
            frame.grid(row=0, column=0, sticky="nsew")
            self.frames[F.__name__] = frame
        self.show_frame("StartPage")

        ### Run Update Checks with show frame
        thread = Thread(target = self.update_check, args = ())
        thread.start()
        
    def set_window_dimensions(self, width, height):
        self.windowW = width
        self.windowH = height
        screen_width = self.container.winfo_screenwidth()
        screen_height = self.container.winfo_screenheight()
        windowX = (screen_width / 2) - (self.windowW / 2)
        windowY = (screen_height / 2) - (self.windowH / 2)
        self.geometry(f'{self.windowW}x{self.windowH}+{int(windowX)}+{int(windowY)}')
        self.minsize(width=self.windowW, height=self.windowH)
        self.maxsize(width=screen_width, height=screen_height)

        self.container.pack(side="top", fill="both", expand = True)
        
    def set_tk_styles(self):
        ### Default Font
        self.default_font = TkFont.nametofont("TkDefaultFont")
        self.default_font.configure(size=13)      

        ### Custom Checkbutton layout
        style=ttk.Style()
        style.layout("TCheckbutton",
            [('Checkbutton.padding', {'sticky': 'nswe', 'children':
                [('Checkbutton.focus', {'side': 'left', 'sticky': '', 'children':
                    [('Checkbutton.indicator', {'side': 'top', 'sticky': 'nswe'})
                    ]
                })]
            })]
        )

        ### Notebook "tabs" styling
        style.layout("Tab",
        [('Notebook.tab', {'sticky': 'nswe', 'children':
            [('Notebook.padding', {'side': 'top', 'sticky': 'nswe', 'children':
                #[('Notebook.focus', {'side': 'top', 'sticky': 'nswe', 'children':
                    [('Notebook.label', {'side': 'top', 'sticky': ''})],
                #})],
            })],
        })]
        )
        
        ### Combobox dropdown - style to default font
        self.option_add("*TCombobox*Listbox*font", (self.default_font))
        
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        frame.update()
        frame.event_generate("<<ShowFrame>>")
    
    '''
    def get_frame(self, name):
        for frame in self.frames:
                if frame.__name__ == name:
                    return frame
    '''
    
    #init text log
    def update_check(self):        
        ### Check if CSS Patched
        ### Check for new version
        self.frames["StartPage"].text1.config(state='normal')
        if is_connected():
            #deprecated         
            #check_if_css_patched(self.frames["StartPage"])
            release_check(self.frames["StartPage"], self.release)
            print("Checking for small updates...")
            thread = Thread(target = self.small_update_check, args = ())
            thread.start()
        else:
            print("You are offline, cannot automatically check for updates.", file=sys.stderr)


    def small_update_check(self):
        file_dates = backend.hash_compare_small_update_files(
            backend.check_new_commit_dates(self.json_data),
            self.json_data)
        #print(file_dates)
        files_no = 0
        for update_type in file_dates:
            files_no += len(file_dates[update_type])
        if files_no > 0:
            thread = Thread(target = UpdateWindow, kwargs = ({'controller': self, 'file_dates': file_dates}))
            thread.start()
        else:
            print("Done.")



class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.controller = controller
        
    ### LOG FRAME
    ### Created first
        self.create_log_frame()

    ### load JSON
        self.controller.json_data = backend.get_json_data()
        self.controller.oldglory_config = backend.load_config()

    ### HEAD FRAME
    ###
        self.frameHead = head_frame(self, self.controller)

    ### Tabs
        self.tabs = ttk.Notebook(self,width=722)
        self.frameCheck = tk.Frame(self.tabs)
        self.framePatch = tk.Frame(self.tabs)
    
    ### Functions - Frames and Pack
        self.create_check_frame()
        self.create_patch_frame()
        self.create_mode_frame()
        self.create_confirm_frame()
        self.set_init_gui_states()
        self.pack_frames()

    def create_log_frame(self):
    ### LOG FRAME
    ### Defined first even though it will be packed after the CHECK FRAME,
    ### due to redirecting StdOut
    ###
        self.frameLog = tk.Frame(self, 
                            width=self.controller.windowW-50, 
                            height=self.controller.windowH-450)
        self.frameLog.grid_propagate(False)
        self.frameLog.columnconfigure(0, weight=1)
        self.frameLog.rowconfigure(0, weight=1)

        ### Text
        entry1 = ttk.Entry(self.frameLog)
        self.text1 = tk.Text(entry1, width=500)
        self.text1.configure(font=("Arial",10))

        ### REDIRECT STDOUT STDERR
        if not DEBUG_STDOUT_STDERR:
            sys.stdout = custom_tk.StdoutRedirector(self.text1)
            sys.stderr = custom_tk.StderrRedirector(self.text1)
        
        self.text1.pack(expand="yes")
        entry1.grid(row=0, column=0)

        ###
        scroll_1 = ttk.Scrollbar(self.frameLog, command=self.text1.yview)
        scroll_1.grid(row=0, column=1, sticky='ns')
        self.text1['yscrollcommand'] = scroll_1.set
        
    def create_check_frame(self):  
    ### CHECK FRAME
    ###
        
        #self.frameCheck.grid_columnconfigure(2, weight=1)

        ######
        self.var1 = tk.IntVar()
        self.check1 = ttk.Checkbutton(self.frameCheck,
                                 variable=self.var1)                        
        self.check1.bind("<Button-1>", lambda event:css_cb_check(event, self.var1, [self.check2, self.check3, self.check5, self.check7]))
        self.check1.grid(row=0, column=0)
        ###        
        mo1 = MainOption(
            parentFrame=self.frameCheck,
            page=self,
            name="Install CSS Tweaks",
            image="images/full_layout.png",
            tags=["CSS"])
        mainoption1 = mo1.returnMainOption()
        mainoption1.grid(row=0, column=1, sticky='w')
        
        ######
        self.var2 = tk.IntVar()
        self.check2 = ttk.Checkbutton(self.frameCheck,
                                 variable=self.var2)
        self.check2.grid(row=1, column=0)
        ###
        mo2 = MainOption(
            parentFrame=self.frameCheck,
            page=self,
            name="  \u2937 Box Play Button",
            image="images/play_button_box.png",
            tags=["CSS"])
        mainoption2 = mo2.returnMainOption()
        mainoption2.grid(row=1, column=1, sticky='w')
        
        ######
        self.var3 = tk.IntVar()
        self.check3 = ttk.Checkbutton(self.frameCheck,
                                 variable=self.var3)
        self.check3.bind("<Button-1>", lambda event:css_cb_check(event, self.var3, [self.check4]))
        self.check3.grid(row=2, column=0)
        ###
        mo3 = MainOption(
            parentFrame=self.frameCheck,
            page=self,
            name="  \u2937 Vertical Nav Bar",
            image="images/vertical_nav_bar.png",
            tags=["CSS"])
        mainoption3 = mo3.returnMainOption()
        mainoption3.grid(row=2, column=1, sticky='w')
        
        ######
        self.var4 = tk.IntVar()
        self.check4 = ttk.Checkbutton(self.frameCheck,
                                 variable=self.var4)
        self.check4.grid(row=3, column=0)
        ###
        mo4 = MainOption(
            parentFrame=self.frameCheck,
            page=self,
            name="    \u2937 Classic Layout",
            image="images/classic_layout.png",
            tags=["CSS"])
        mainoption4 = mo4.returnMainOption()
        mainoption4.grid(row=3, column=1, sticky='w')
        
        ######
        self.var5 = tk.IntVar()
        self.check5 = ttk.Checkbutton(self.frameCheck,
                                 variable=self.var5)
        self.check5.grid(row=4, column=0)
        ###
        mo5 = MainOption(
            parentFrame=self.frameCheck,
            page=self,
            name="  \u2937 Landscape Game Images",
            image="images/landscape_images.png",
            tags=["CSS", "JS"])
        mainoption5 = mo5.returnMainOption()
        mainoption5.grid(row=4, column=1, sticky='w')

        ######
        self.change_theme = 0
        self.var6 = tk.IntVar()
        self.check6 = ttk.Checkbutton(self.frameCheck,
                                 variable=self.var6)
        self.check6.bind("<Button-1>", lambda event: self.setChangeTheme(event))
        self.check6.grid(row=5, column=0)
        ###
        mo6 = MainOption(
            parentFrame=self.frameCheck,
            page=self,
            name="Library Theme",
            image="images/theme_shiina.png",
            tags=["CSS"])
        mainoption6 = mo6.returnMainOption()
        mainoption6.grid(row=5, column=1, sticky='w')
        
        ###
        self.dropdown6_value = tk.StringVar()
        self.dropdown6 = ttk.Combobox(self.frameCheck,
                                 font="TkDefaultFont",
                                 values=self.getListOfThemeNames(self.controller),
                                 state="readonly",
                                 textvariable=self.dropdown6_value,
                                 width=30)
        self.dropdown6.current(0)
        self.dropdown6.bind("<<ComboboxSelected>>", lambda event: dropdown_click(event, self, self.controller))
        self.dropdown6.grid(row=6, column=1, columnspan=2, sticky="w")

        ######
        self.var7 = tk.IntVar()
        self.check7 = ttk.Checkbutton(self.frameCheck,
                                 variable=self.var7)
        self.check7.grid(row=0, column=2)
        ###
        mo7 = MainOption(
            parentFrame=self.frameCheck,
            page=self,
            name="Classic Styling (WIP)",
            image="images/classic_styling.png",
            tags=["CSS"])
        mainoption7 = mo7.returnMainOption()
        mainoption7.grid(row=0, column=3, sticky='w')

        ######
        self.var8 = tk.IntVar()
        self.check8 = ttk.Checkbutton(self.frameCheck,
                                 variable=self.var8)
        self.check8.grid(row=1, column=2)
        ###
        mo8 = MainOption(
            parentFrame=self.frameCheck,
            page=self,
            name="Home Button Icon",
            image="images/home_button.png",
            tags=["CSS"])
        mainoption8 = mo8.returnMainOption()
        mainoption8.grid(row=1, column=3, sticky='w')


        ###
        #self.image1 = add_img(self.frameCheck, os.path.join(os.getcwd(), 'images/full_layout.png'))
        #self.image1.grid(row=0, column=4, rowspan=8, padx=5, sticky="n")      
    
    def create_patch_frame(self):
    ### PATCH FRAME
    ###
        
        labeltext_a = tk.StringVar()
        labeltext_a.set("Quick Links")
        
        label_a = tk.Label(self.framePatch, textvariable=labeltext_a)
        label_a.grid(row=0, column=0)
        
        pbutton1 = ttk.Button(self.framePatch,
                              text="Open OldGlory folder",
                              width=22
        )
        pbutton1.bind("<Button-1>", lambda event:backend.OS_open_file(os.getcwd()))
        pbutton1.grid(row=1, column=0, padx=(5,0), pady=5)

        pbutton2 = ttk.Button(self.framePatch,
                              text="Open steamui folder",
                              width=22
        )
        pbutton2.bind("<Button-1>", lambda event:backend.OS_open_file(backend.library_dir()))
        pbutton2.grid(row=2, column=0, padx=(5,0), pady=5)


        labeltext_b = tk.StringVar()
        labeltext_b.set("steam-library (Shiina)")
        
        label_b = tk.Label(self.framePatch, textvariable=labeltext_b)
        label_b.grid(row=3, column=0)
        
        pbutton3 = ttk.Button(self.framePatch,
                              text="Apply config.css",
                              width=22
        )
        button3_tip = custom_tk.Detail_tooltip(pbutton3,
                                     "If you have modifed themes/config.css for steam-library,\n" \
                                     "click here to copy it over to steamui",
                                     hover_delay=200)
        pbutton3.bind("<Button-1>", lambda event:backend.steam_library_compat_config(1))
        pbutton3.grid(row=4, column=0, padx=(5,0), pady=5)
        
        labeltext_c = tk.StringVar()
        labeltext_c.set("Patching")
        
        label_c = tk.Label(self.framePatch, textvariable=labeltext_c)
        label_c.grid(row=0, column=1)
        
        pbutton4 = ttk.Button(self.framePatch,
                              text="Patch CSS",
                              width=22
        )
        button4_tip = custom_tk.Detail_tooltip(pbutton4,
                                     "Alternative to SFP for patching CSS",
                                     hover_delay=200)
        pbutton4.bind("<Button-1>", lambda event:backend.patch_css())
        pbutton4.grid(row=1, column=1, padx=(5,0), pady=5)
    
        
    def create_mode_frame(self):   
    ### MODE FRAME
    ###
        self.frameMode = tk.Frame(self)

        ###
        self.var_m = tk.IntVar()
        button_m = ttk.Button(self.frameMode,
                           text="CSS Options",
                           width=16
        )
        button_m.bind("<Button-1>", lambda event:show_CSSPage(self.controller))
        button_m.grid(row=0, column=0, padx=5)

        ###
        self.var_n = tk.IntVar()
        button_n = ttk.Button(self.frameMode,
                           text="JS Options",
                           width=16
        )
        button_n.bind("<Button-1>", lambda event:show_JSPage(self.controller))
        button_n.grid(row=0, column=1, padx=5)
        
        
    def create_confirm_frame(self):
    ### CONFIRM FRAME
    ###
        self.ConfirmObject = ConfirmFrame(self, self.controller)
        self.frameConfirm = self.ConfirmObject.get_frame_confirm()
           
        
    def set_init_gui_states(self):
    ### Running functions after much of StartPage has been initialised
    ###
        ### Set GUI from config
        self.loaded_config = manager.set_selected_main_options(self, self.controller)
        self.text1.config(state='disabled')
        init_cb_check(self.var1, [self.check2, self.check3, self.check5, self.check7])
        init_cb_check(self.var3, [self.check4])
        

    def pack_frames(self):
    ### Place frames into page
        self.frameHead.pack()
        self.frameCheck.pack()
        self.framePatch.pack()

        ###tabs
        self.tabs.add(self.frameCheck, text="Main Options")
        self.tabs.add(self.framePatch, text="Advanced Options")
        #self.tabs.add(self.framePatch, text="Patching")
        self.tabs.pack(expand=1)
        
        self.frameLog.pack(padx=17, pady=(10,7), expand=1, fill='both')
        self.frameConfirm.pack(pady=(7, 20), side="bottom", fill="x")
        self.frameMode.pack(pady=(2, 0), side="bottom")


    ### Getters
    def getCheck(self, getter):
        return getattr(self, getter)
    def getCheckbuttonVal(self, getter):
        return getattr(self, getter)
    def getTextArea(self, getter):
        return getattr(self, getter)
    def getDropdownVal(self, getter):
        return getattr(self, getter)
    def setChangeTheme(self, event):
        self.change_theme = 1

    def getListOfThemeNames(self, controller):
        themes = []
        try:
            for theme in controller.json_data["themes"].keys():
                #print(theme)
                themes.append(theme + " (" + controller.json_data["themes"][theme]["author"] + ")")
        except Exception as e:
            print("Error loading themes from JSON file. Loading default themes data.",file=sys.stderr)
            print_traceback()
            #default theme data
            for theme in THEME_MAP:
                themes.append(theme)
        
        return themes

class CSSPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

    ### HEAD FRAME
    ###
        self.frameHead = head_frame(self, controller)

    ### Tabs
        tabs = ttk.Notebook(self,)
        frameQuick = tk.Frame(tabs)
        frameSections = tk.Frame(tabs)

    ### CSS Frame
    ###
        controller.css_config = backend.load_css_configurables()
        self.frameCSS = tk.Frame(frameQuick)
        self.css_gui = CSSGUICreator(frameQuick, controller, controller.css_config)
        self.frameCSS = self.css_gui.returnframeCSS()
        
    ### MODE Frame
    ###
        self.frameMode = tk.Frame(self)

        ###
        self.var_m = tk.IntVar()
        button_m = ttk.Button(self.frameMode,
                           text="Back to Home",
                           width=16
        )
        button_m.bind("<Button-1>", lambda event:controller.show_frame("StartPage"))
        button_m.grid(row=0, column=0, padx=5)

        ###
        self.var_n = tk.IntVar()
        button_n = ttk.Button(self.frameMode,
                           text="JS Options",
                           width=16
        )
        button_n.bind("<Button-1>", lambda event:show_JSPage(controller))
        button_n.grid(row=0, column=1, padx=5)

    ### CONFIRM FRAME
    ###
        self.ConfirmObject = ConfirmFrame(self, controller)
        self.frameConfirm = self.ConfirmObject.get_frame_confirm()
        
    ### Pack frames
        self.frameHead.pack()
        self.frameCSS.pack(padx=10, fill="x")
        
        frameQuick.pack()
        frameSections.pack()

        ###tabs
        tabs.add(frameQuick, text="Quick CSS")
        tabs.add(frameSections, text="CSS Sections")
        tabs.pack(fill="both", expand=1, padx=(10,9))
        
        self.frameConfirm.pack(pady=(7, 20), side="bottom", fill="x")
        self.frameMode.pack(pady=(2, 0), side="bottom")

        #self.frameCSS = create_css_gui(self, controller, backend.load_css_configurables())

class JSPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

    ### HEAD FRAME
    ###
        self.frameHead = head_frame(self, controller)

        label_js_head = tk.Label(self, text="JS Options")

    ### JS FRAME
    ###
        controller.js_config, controller.special_js_config = backend.load_js_fixes()
        self.frameJS = tk.Frame(self)
        self.js_gui = JSFrame(self, controller)
        self.frameJS = self.js_gui.returnframeJS()
        
    ### MODE Frame
    ###
        self.frameMode = tk.Frame(self)

        ###
        self.var_m = tk.IntVar()
        button_m = ttk.Button(self.frameMode,
                           text="Back to Home",
                           width=16
        )
        button_m.bind("<Button-1>", lambda event:controller.show_frame("StartPage"))
        button_m.grid(row=0, column=0, padx=5)

        ###
        self.var_n = tk.IntVar()
        button_n = ttk.Button(self.frameMode,
                           text="CSS Options",
                           width=16
        )
        button_n.bind("<Button-1>", lambda event:show_CSSPage(controller))
        button_n.grid(row=0, column=1, padx=5)
    
    ### CONFIRM FRAME
    ###
        self.ConfirmObject = ConfirmFrame(self, controller)
        frameConfirm = self.ConfirmObject.get_frame_confirm()

    ### Pack frames
    ###
        self.frameHead.pack()
        label_js_head.pack()
        self.frameJS.pack(padx=10, expand=1, fill="both")
        frameConfirm.pack(pady=(7, 20), side="bottom", fill="x")
        self.frameMode.pack(pady=(2, 0), side="bottom")

### FRAME functions
### ================================

### HEAD FRAME
###
def head_frame(self, controller):

    frameHead = tk.Frame(self)
        
    ###
    titlefont = controller.default_font.copy()
    titlefont.configure(size=20)
        
    labeltext_a = tk.StringVar()
    labeltext_a.set("SteamUI-OldGlory")
        
    label_a = tk.Label(frameHead, textvariable=labeltext_a, font=titlefont)
    label_a.grid(row=0, column=0)

    ###
    self.labeltext_b = tk.StringVar()
    self.labeltext_b.set("A set of CSS and JS tweaks for the Steam Library")
        
    label_b = tk.Label(frameHead, textvariable=self.labeltext_b)
    label_b.grid(row=1, column=0)
    return frameHead

### CONFIRM FRAME
###
class ConfirmFrame(tk.Frame):
    def __init__(self, page, controller):
        self.frameConfirm = tk.Frame(page)        
        self.frameConfirm.grid_columnconfigure(0, weight=1)
        self.frameConfirm.grid_columnconfigure(1, weight=0)
        self.frameConfirm.grid_columnconfigure(2, weight=0)
        self.frameConfirm.grid_columnconfigure(3, weight=1)

        ###
        self.left_frame = tk.Frame(self.frameConfirm,
                                   width=3)
                
        ###
        self.install_modes = ("CSS Only", "CSS + JS", "CSS/JS")
        self.modeVar = tk.StringVar()
        
        self.modeMenu = ttk.OptionMenu(self.left_frame,
                        self.modeVar,
                        self.install_modes[2],
                        *self.install_modes   
        )
        self.modeMenu.config(width=8, state='disabled')
        #self.modeMenu.bind("<Button-1>",
        #             lambda event:manager.install_click(event, controller.frames["StartPage"], controller)
        #             )
        self.modeMenu.grid(row=0, column=0, padx=5)
        
        self.left_frame.grid(row=0, column=0, sticky=tk.E)
        
        
        
        
        ###
        self.button1 = ttk.Button(self.frameConfirm,
                        text="Install",
                        width=16                      
        )
        self.button1.bind("<Button-1>",
                    lambda event:manager.install_click(event, controller.frames["StartPage"], controller)
                    )
        self.button1.grid(row=0, column=1, padx=5, sticky="NSEW")
                
        ###
        button2 = ttk.Button(self.frameConfirm,
                        text="Reload Config",
                        width=16#,
                        ###state='disabled'
        )
        button2_tip = custom_tk.Detail_tooltip(button2, "If you have modified the files manually,\nclick here to reload their values into the program.", hover_delay=200)
        button2.bind("<Button-1>",
                    lambda event:reload_click(event, controller)
                    )
        button2.grid(row=0, column=2, padx=5, sticky="NSEW")

        ###
        settings_image = open_img(os.path.join(os.getcwd(), 'images/settings.png'), 24)
        button3 = ttk.Button(self.frameConfirm,
                        #text="GG",
                        image=settings_image,
                        width=3#,
                        ###state='disabled'
        )
        button3.image = settings_image
        button3_tip = custom_tk.Detail_tooltip(button3, "Settings and About", hover_delay=200)
        button3.bind("<Button-1>",
                    lambda event:settings_window(event, controller)
                    )
        button3.grid(row=0, column=3, padx=(65,15), sticky=tk.E)
    
    def disable_install_button(self):
        self.button1['state'] = 'disable'
        self.button1.configure(text="Installing...")
        
    def enable_install_button(self):
        self.button1['state'] = 'normal'
        self.button1.configure(text="Install")
    
    def get_install_button(self):
        return self.button1
    
    def get_frame_confirm(self):
        return self.frameConfirm
    
    def set_mode_menu(self, index):
        self.modeVar.set(self.install_modes[index])
        #print(index)
        
    def get_mode_menu(self):
        return self.modeVar
        
### ================================

### Show Page Functions
### ================================
def show_CSSPage(controller):
    #controller.css_config = backend.load_css_configurables()
    controller.show_frame("CSSPage")
    #controller.frames["CSSPage"].frameCSS = create_css_gui(controller.frames["CSSPage"], controller, backend.load_css_configurables())
    #update_css_gui(controller.frames["CSSPage"], controller, controller.css_config)
def show_JSPage(controller):
    #controller.js_config = backend.load_js_fixes()
    controller.show_frame("JSPage")

### ================================
### Initialisation
### ================================

### Check Internet
def is_connected():
    try:
        socket.create_connection(("1.1.1.1", 53))
        return True
    except OSError:
        pass
    return False

### Check SteamFriendsPatcher
def check_if_css_patched(page):
    if not backend.is_css_patched("2.css"):
        hyperlink = custom_tk.HyperlinkManager(page.text1)
        page.text1.tag_configure("err", foreground="red")
        page.text1.insert(tk.INSERT, '\n==============================\n')
        page.text1.insert(tk.INSERT, "css/5.css (previously known as libraryroot.css) not patched.\n", ("err"))
        page.text1.insert(tk.INSERT, "Download ")
        page.text1.insert(tk.INSERT, "SteamFriendsPatcher\n", hyperlink.add(partial(webbrowser.open, "https://github.com/PhantomGamers/SteamFriendsPatcher/")))
        page.text1.insert(tk.INSERT, '==============================\n')
### Check if newer version
def release_check(page, current_release):
    try:
        session = backend.create_session()        
        response = session.get("https://api.github.com/repos/jonius7/steamui-oldglory/releases/latest", timeout=0.5)
        latest_release = response.json()["name"]
        #print(re.sub("[^0-9.]+", "", current_release))
        if latest_release == current_release:
            page.text1.insert(tk.INSERT, "You are up to date. Release " + latest_release + "\n")
        else:
            hyperlink = custom_tk.HyperlinkManager(page.text1)
            page.text1.insert(tk.INSERT, '\n==============================\n')
            page.text1.insert(tk.END, 'New version available: ')
            page.text1.insert(tk.END, "Release {0}".format(latest_release), hyperlink.add(partial(webbrowser.open, "https://github.com/Jonius7/SteamUI-OldGlory/releases/latest")))
            page.text1.insert(tk.END, '\nCurrent version: ')
            page.text1.insert(tk.END, "Release {0}\n".format(current_release))
            page.text1.insert(tk.INSERT, '==============================\n\n')
    except KeyError:
        print("Unable to get latest version number, too many requests! Please try again later.", file=sys.stderr)
    except requests.exceptions.ConnectionError:
        print("Could not connect to Github, Unable to check for latest release!", file=sys.stderr)
    except socket.timeout:
        print("Update check timeout!", file=sys.stderr)
    except AttributeError:
        print("Could not connect to Github, Unable to check for latest release!", file=sys.stderr)
    except Exception as e:
        print("Unable to check for latest release!", file=sys.stderr)
        print(e.message, file=sys.stderr)
    

   
### Checkbox Validation - Disable
### ================================
### still the two functions, instead of 1, probably due to init
def css_cb_check(event, var1, checks):
    if var1.get() == 0:
        for check in checks:
            check.config(state='normal')
    else:
        for check in checks:
            check.config(state='disabled')
        
def init_cb_check(var1, checks):
    if var1.get() == 1:
        for check in checks:
            check.config(state='normal')
    else:
        for check in checks:
            check.config(state='disabled')
### ================================


### MainOption
### ================================
### Label + CodeTag
### Kwargs expected:
### parentFrame, page, name, image, tags
class MainOption(tk.Frame):
    def __init__(self, **kwargs):
        self.parentFrame = kwargs["parentFrame"]
        self.page = kwargs["page"]
        self.name = kwargs["name"]
        self.image = kwargs["image"]
        self.tags = {}
        self.tagFrame = tk.Frame(self.parentFrame)
        self.label = tk.Label(self.tagFrame,
                              text=self.name,
                              cursor="hand2")
        
        #self.label.bind("<Button-1>", lambda event: globals()["change_image"](self.page.image1, os.path.join(os.getcwd(), self.image)))
        #self.label.bind("<Enter>", lambda event: globals()["change_image"](self.page.image1, os.path.join(os.getcwd(), self.image)))
        self.tip = custom_tk.Image_tooltip(self.label, globals()["open_img"](self.image), hover_delay=400)
    
        self.label.grid(row=0, column=0, sticky='w')

        self.create_tags(kwargs["tags"])
        
    def create_tags(self, tagnames):
        for i, tagName in enumerate(tagnames, start=1):
            leftPadding = (5, 0) if i == 1 else 0
            tag = add_img(self.tagFrame, os.path.join(os.getcwd(), 'images/tag_'+tagName+'.png'), width=50)
            tag.grid(row=0, column=i, sticky='w', padx=leftPadding)
            self.tags[self.name]=tag
            
    def returnMainOption(self):
        return self.tagFrame

### Dropdown click (theme)
### This is a backup list - .json provides an updated theme list
###
THEME_MAP = {
    "steam-library (Shiina)" : {
        "filename" : "shiina.css",
        "order" : "before",
    },
    "Dark Library (Thespikedballofdoom)" : {
        "filename" : "spiked.css",
        "order" : "after"
    },
    "Acrylic Theme (EliteSkylu)" : {
        "filename" : "acrylic.css",
        "order" : "after"
    },
    "Crisp Cut" : {
        "filename" : "crispcut.css",
        "order" : "after"
    }
}

def dropdown_click(event, page, controller):
    theme_name = event.widget.get()
    #print(theme_name)
    #print(controller.json_data["themes"][theme_name.split(" (")[0]]["filename"])
    
    #theme_image_path = os.path.join(os.getcwd(), "images/theme_" + controller.json_data["themes"][theme_name.split(" (")[0]]["filename"][1:-5] + ".png")
    theme_image_path = os.path.join(os.getcwd(), "themes", theme_name.split(" (")[0], "preview.png")
    dropdown_hover(theme_image_path, event.widget)

def dropdown_hover(image_path, widget):
    if os.path.isfile(image_path):
        tip = custom_tk.Image_tooltip(widget, open_img(image_path), hover_delay=100)
    else:
        print("Theme preview image not found at: " + image_path + ",\n  using default No Preview image")
        tip = custom_tk.Image_tooltip(widget, open_img(os.path.join(os.getcwd(), "images/no_preview.png")), hover_delay=100)

MAIN_SETTINGS_MAP = {
    "InstallCSSTweaks" : {"value" : "var1", "javascript" : False},
    "EnablePlayButtonBox" : {"value" : "var2", "javascript" : False},
    "EnableVerticalNavBar" : {"value" : "var3", "javascript" : False},
    "EnableClassicLayout" : {"value" : "var4", "javascript" : False},
    "LandscapeImages" : {"value" : "var5", "javascript" : True},
    "InstallWithLibraryTheme" : {"value" : "var6", "javascript" : False},
    "ClassicStyling" : {"value" : "var7", "javascript" : False},
    "ThemeSelected" : {"set" : ""}
    }

def run_js_tweaker(controller, reset=0, max_stage=10):
    try:
        text_area = controller.frames["StartPage"].text1
        print("==============================")
        print("Running js_tweaker")
        text_area.update_idletasks()
        ###
        if max_stage >= 1:
            run_and_update_tkinter(lambda: js_tweaker.initialise(), text_area)
            run_and_update_tkinter(lambda: js_tweaker.copy_files_from_steam(reset), text_area)
            run_and_update_tkinter(lambda: js_tweaker.backup_files_from_steam(), text_area)
            #run_and_update_tkinter(lambda: js_tweaker.setup_library(), text_area)
            run_and_update_tkinter(lambda: js_tweaker.modify_html(), text_area)
        if max_stage >= 2:
            run_and_update_tkinter(lambda: js_tweaker.beautify_js(), text_area)
            run_and_update_tkinter(lambda: js_tweaker.beautify_js(controller.json_data["libraryjsFile"]), text_area)
            run_and_update_tkinter(lambda: js_tweaker.beautify_js(controller.json_data["jsFile"]), text_area)
            run_and_update_tkinter(lambda: js_tweaker.parse_fixes_file("fixes.txt"), text_area)
        if max_stage >= 3:
            run_and_update_tkinter(lambda: js_tweaker.write_modif_file(), text_area)
            run_and_update_tkinter(lambda: js_tweaker.write_modif_file(controller.json_data["libraryjsFile"]), text_area)
            run_and_update_tkinter(lambda: js_tweaker.write_modif_file(controller.json_data["jsFile"]), text_area)
            run_and_update_tkinter(lambda: js_tweaker.re_minify_file(), text_area)
            run_and_update_tkinter(lambda: js_tweaker.re_minify_file(controller.json_data["libraryjsModifFile"], controller.json_data["libraryjsPatchedFile"]), text_area)
            run_and_update_tkinter(lambda: js_tweaker.re_minify_file(controller.json_data["jsModifFile"], controller.json_data["jsPatchedFile"]), text_area)
        if max_stage >= 4:
            run_and_update_tkinter(lambda: js_tweaker.compress_newlines(controller.json_data["libraryjsPatchedFile"]), text_area)
            run_and_update_tkinter(lambda: js_tweaker.compress_newlines(controller.json_data["libraryrootjsPatchedFile"]), text_area)
            run_and_update_tkinter(lambda: js_tweaker.copy_files_to_steam(), text_area)
            print("\nSteam Library JS Tweaks applied successfully.")         
    except Exception as e:
        print("Error while applying JS Tweaks.", file=sys.stderr)
        print_traceback()

def run_and_update_tkinter(func, widget):
    value = func()
    widget.update_idletasks()
    return value
                              
### ================================


### RELOAD Functions
### ================================
def reload_click(event, controller):
    try:
        print("==============================")
        ### Reload Data
        controller.frames["StartPage"].loaded_config = manager.set_selected_main_options(controller.frames["StartPage"], controller)
        print("Loaded config data. (oldglory_config.cfg)")
        #print("Loaded config data. (oldglory_config2.cfg)")
        controller.json_data = backend.get_json_data()
        controller.css_config = backend.load_css_configurables()
        controller.js_config, controller.special_js_config = backend.load_js_fixes()
        ### Update GUI
        controller.frames["CSSPage"].css_gui.PresetFrame.update_presets_gui()
        controller.frames["JSPage"].js_gui.update_js_gui(controller)
        print("Config Reloaded.")
    except:
        print("Config could not be completely reloaded.", file=sys.stderr)
        print_traceback()
### ================================


### Image Functions
### ================================
def open_img(filename, width=350):
    try:
        if os.path.isfile(filename):
            x = filename
            img = Image.open(x)
            new_width = width
            new_height = int(new_width * img.height / img.width)
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            img = ImageTk.PhotoImage(img)
            return img
    except:
        print("Unable to add image: " + filename, file=sys.stderr)
        print_traceback()

def add_img(frame, filename, width=350):
    img = open_img(filename, width)
    panel = tk.Label(frame, image=img)
    panel.image = img
    return panel 
        
def change_image(label, filename):
    img = open_img(filename)
    label.configure(image=img)
    label.image = img
### ================================

### CSS Options Functions
### ================================
### CSS Config to GUI
class CSSGUICreator(tk.Frame):
    def __init__(self, page, controller, config):
        self.page = page
        self.controller = controller
        self.config = config
        ###Outer frame and canvas
        self.frameCSS = custom_tk.ScrollFrame(page)
        
        self.PresetFrame = PresetFrame(self.frameCSS, controller, config)
        self.framePreset = self.PresetFrame.returnPresetFrame()
        self.PresetFrame.getPresetOptions()

        #Configure grid expand
        self.frameCSS.columnconfigure(0, weight=2)
        self.frameCSS.rowconfigure(0, weight=1)
        self.frameCSS.columnconfigure(1, weight=1)
        
        self.framePreset.grid(row=0, column=0, sticky="nsew")
        #self.frameConfigurables.grid(row=0, column=1, sticky="nsew")
        #frameConfigurables.pack(fill="both", expand=True, padx=10)
    def returnframeCSS(self):
        return self.frameCSS

###Structure of CSS config as follows
###config       > section       > prop              > attr
###CSS_CONFIG   > "What's New"  > "--WhatsNewOrder" > "desc"
class CSSConfigRow(tk.Frame):
    def __init__(self, propName, propDict, parentFrame):
        self.propName = propName
        self.propDict = propDict
        self.parentFrame = parentFrame
        self.frameCSSRow = tk.Frame(self.parentFrame)
        try:
            
            self.label = tk.Label(self.frameCSSRow,
                              text=self.propName,anchor='w',width=25)
            tip = custom_tk.Detail_tooltip(self.label, formatted_hover_text(self.propDict['default'], self.propDict['desc']), hover_delay=200)
            
            self.label.grid(row=0, column=0)
            
            self.combobox = ttk.Combobox(self.frameCSSRow,
                                    font="TkDefaultFont",
                                     values=get_prop_options_as_array(self.propDict),
                                    width=12)
            self.combobox.set(self.propDict['current'])
            self.combobox.grid(row=0, column=1, pady=1)
        
        except Exception as e:
            print("CSS config in libraryroot.custom.css not configured correctly.\n", file=sys.stderr)
            print("Either the format of configurable variables is incorrect or this feature is not fully implemented yet.\n", file=sys.stderr)
            print_traceback()

    def returnCSSConfigRow(self):
        return self.frameCSSRow

###
### END ConfigurablesFrame


DEFAULT_QUICK_CSS = {"Top of Page" : {"value" : "1", "config" :
                            {"--WhatsNew" : "block",
                            "--WhatsNewOrder" : "0"}},
                              "Bottom of page" : {"value" : "2", "config" : 
                            {"--WhatsNew" : "block",
                            "--WhatsNewOrder" : "2"}},
                  "Hide entirely" : {"value" : "3", "config" :
                            {"--WhatsNew" : "none",
                            "--WhatsNewOrder" : "0"}},
                    "[Current value]" : {"value" : "4"}
                    }


### START PresetFrame
class PresetFrame(tk.Frame):
    def __init__(self, parent, controller, config):
        self.parent = parent
        self.framePreset = tk.Frame(self.parent)
        self.controller = controller
        self.config = config #unused?
        self.presetOptions = {}
            
        #label_preset_head = tk.Label(self.framePreset, text="Quick CSS Options (more coming soon)")
        #label_preset_head.grid(row=0, column=0, sticky="nsew")


    def getPresetOptions(self):
        try:
            if "quickCSS" in self.controller.json_data:
                #print("quickCSS found")
                #print(self.controller.json_data)

                for i, presetOption in enumerate(self.controller.json_data["quickCSS"]):
                    #print(self.controller.json_data["quickCSS"][presetOption])
                    _p = PresetOption(self.framePreset, self.controller, presetOption, self.controller.json_data["quickCSS"][presetOption])
                    _p.returnPresetOption().grid(row=i // 3, column=i % 3, padx=(5,0), pady=(0,18), sticky="nw")
                    self.presetOptions[presetOption] = _p

                self.createFrameLinks()
                    
            else:
                raise Exception("Property quickCSS in JSON file not found.\n"\
                                "Unable to load Quick CSS Options.")
        except:
            print_traceback()
            
    def createFrameLinks(self):
        ### Links frame
        frameLinks = tk.Frame(self.framePreset)
        #
        var_file_path = os.path.join(os.getcwd(), "variables.css")
        button_vars = ttk.Button(frameLinks,
                            text="Open variables file",
                            width=16
        )
        button_vars.bind("<Button-1>", lambda event:backend.OS_open_file(var_file_path))
        button_vars.grid(row=0, column=0, padx=(5,0), pady=(0,5))

        #
        scss_file_path = os.path.join(os.getcwd(), "scss", "libraryroot.custom.scss")
        button_scss = ttk.Button(frameLinks,
                            text="Open scss file",
                            width=16
        )
        button_scss.bind("<Button-1>", lambda event:backend.OS_open_file(scss_file_path))
        button_scss.grid(row=1, column=0, padx=(5,0), pady=(0,5))

        #
        last_option_num = len(self.controller.json_data["quickCSS"])
        frameLinks.grid(row=last_option_num // 3, column=last_option_num % 3, padx=(5,0))

    def clearPresetOptions(self):
        self.presetOptions.clear()
        for widget in self.framePreset.winfo_children():
            widget.destroy()

    def update_presets_gui(self):
        self.clearPresetOptions()
        self.getPresetOptions()
        
    ###    
    def returnPresetFrame(self):
        return self.framePreset

###
### END PresetFrame


### START PresetOption
class PresetOption(tk.Frame):

    def __init__(self, parent, controller, name, data):
        self.parent = parent
        self.framePresetOption = tk.Frame(self.parent)
        self.controller = controller
        self.name = name
        self.data = data

        #
        smallfont = controller.default_font.copy()
        smallfont.configure(size=12)

        style = ttk.Style()
        style.configure("TRadiobutton", font=smallfont)
        
    ###
        self.preset_title = tk.Label(self.framePresetOption,
                                     text="\u23af\u23af\u23af " + name + " \u23af\u23af\u23af",
                                     font=smallfont)
        self.preset_title.grid(row=0, column=0, sticky='w')


    ###
        self.radiovar = tk.StringVar()
        self.set_preset_default()

        self.radios = []
        
        for i, (textv, value) in enumerate(self.data.items(), 1):
            _radio = ttk.Radiobutton(self.framePresetOption,
                            text = textv, 
                            variable = self.radiovar,
                            value = value["value"],
                            command = lambda textv = textv: self.preset_click(controller, textv)
                            )
            _radio.grid(row=i+1, column=0, padx=(5,0), sticky='w')
            #
            tip = custom_tk.Detail_tooltip(_radio, self.radio_hover_text(textv, value), hover_delay=200)
            #
            self.radios.append(_radio)

    def radio_hover_text(self, key, value):
        tip = ""
        if "config" in value:
            for prop in value["config"]:
                tip += prop + ": " + value["config"][prop] + "\n"
            tip = tip[0:-1]
        elif key == "[Current value]":
            tip += "Keep current value. Can be a custom value set manually in file."
        else:
            tip += "No description."
        return tip

    ### set selected based on value in css_config
    def set_preset_default(self):
        #print(self.controller.css_config)
        key_set = 0
        for key in self.data:
            equal = False
            if "config" in self.data[key]:
                equal = True
                for prop in self.data[key]["config"]:
                    #print(prop)
                    #print("KEY : VALUE")
                    
                    #if value in self.radios_config matches value in css_config
                    equal = (self.data[key]["config"][prop] == get_item(prop, self.controller.css_config)) and equal
                    #print((self.radios_config[key]["config"][prop] == get_item(prop, self.controller.css_config)))
                    #print(self.radios_config[key]["config"][prop])
                    #print(get_item(prop, self.controller.css_config))
                    ##print(prop + " : " + get_item(prop, self.controller.css_config))
            #print(key + " | " + str(equal))
            if equal:
                self.radiovar.set(self.data[key]["value"])
                key_set = 1
        if key_set == 0:
            self.radiovar.set(self.data["[Current value]"]["value"])

        ### PRESET Click funtion
    def preset_click(self, controller, radioText):
        #print(radioText)
        if radioText != "[Current value]":
            globals()["apply_css_config_values"](controller, self.data[radioText]["config"])
        #print(controller.css_config)

    def returnPresetOption(self):
        return self.framePresetOption
    
###
### END PresetOption

### Preset
### ~~~~~~~~~~
### change container.css_config
### Recursion
def apply_css_config_values(controller, propValues):
    returns = []
    for key, value in propValues.items():
        controller.config_dict = replace_item(key, value, controller.css_config)

            
### Recursion 
        #key, replace_value obj
def replace_item(key, value, config_dict):
    for k, v in config_dict.items():
        if isinstance(v, dict):
            config_dict[k] = replace_item(key, value, v)
    if key in config_dict:
        config_dict[key]["current"] = value
    return config_dict

### Recursion
def get_item(key, config_dict):
    if key in config_dict:        
        return config_dict[key]["current"]
    for value in config_dict.values():
        if isinstance(value, dict):
            ret = get_item(key, value)
            if ret:
                return ret

###
### END PresetOption

def update_css_gui(page, controller, config):
    test_css_gui_reach(page, controller, config)
    #for entrybox in page.css_gui.entryboxes:
        #config.get(sectionkey, {}).get(propkey)

def test_css_gui_reach(page, controller, config):
    pass

def formatted_hover_text(default, desc):
    return "Default: " + default + ". " + desc

def get_prop_options_as_array(propDict):
    try:
        optionsarray = []
        for option in propDict['options']:
            optionsarray.append(option)
        return optionsarray
    except:
        print("Options Invalid", file=sys.stderr)

###
class JSFrame(tk.Frame):
    def __init__(self, page, controller):
        self.frameJS = custom_tk.ScrollFrame(page)
        self.controller = controller
        self.frameJSInner = tk.Frame(self.frameJS.content)

        self.checkvars = {}
        self.comboboxes = {}
        
        self.create_frameJSInner(self.controller)
        self.frameJSInner.grid(row=1, column=0)

    ### PRESET Click funtion
    def js_click(self, controller, fixname):
        try:
            controller.js_config[fixname] = str(self.checkvars[fixname].get())
            self.controller.js_gui_changed = 1
            manager.set_mode_menu_var(self.controller, self.controller.js_gui_changed)
            #print(controller.js_config)
        except Exception as e:
            print("Error setting config :\n"\
                  "Fix:   " + fixname, file=sys.stderr)
            
    def create_frameJSInner(self, controller):
        rownum = 1
        self.checkvars = {}
        self.comboboxes = {}
        for i, (fixname, value) in enumerate(self.controller.js_config.items()):
            _checkvar = tk.IntVar()
            self.checkvars[fixname] = _checkvar
            self.checkvars[fixname].set(int(value))
            _checkbutton = ttk.Checkbutton(self.frameJSInner,
                            text = fixname,
                            variable = _checkvar,
                            command = lambda fixname = fixname: self.js_click(self.controller, fixname)
                            )
            _label = tk.Label(self.frameJSInner,
                              text=fixname,
                              cursor="hand2")
            #_label.bind("<Button-1>", lambda event: globals()["change_image"](self.page.image1, os.path.join(os.getcwd(), self.image)))

            _checkbutton.grid(row=rownum, column=0, padx=(5,0), sticky='w')
            _label.grid(row=rownum, column=1, sticky='w')
            
            rownum += 1
            if fixname in self.controller.special_js_config:
                #print(self.controller.special_js_config["Change Game Image Grid Sizes (optional) - default widths 111, 148, 222"])
                self.sizesFrame = tk.Frame(self.frameJSInner)
                special_js_key_name = fixname
                for i, key in enumerate(self.controller.special_js_config[special_js_key_name]):
                    _combolabel = tk.Label(self.sizesFrame,
                                          text = key)
                    _combobox = ttk.Combobox(self.sizesFrame,
                                font="TkDefaultFont", 
                                 values=self.controller.special_js_config[special_js_key_name][key],
                                width=6)
                    
                    _combobox.set(self.controller.special_js_config[special_js_key_name][key])
                    _combobox.bind("<Button-1>", lambda event: self.combobox_changed(event, self.controller))
                    #_combobox.bind("<<ComboboxSelected>>", lambda fixname = fixname, propname = propname: combobox_changed(controller, fixname, key))
                    _combolabel.grid(row=0, column=2*i, padx=(0,5))
                    _combobox.grid(row=0, column=2*i+1, padx=(0,15))
                    self.comboboxes[key] = _combobox
                self.sizesFrame.grid(row=rownum, column=1, sticky='w')
                rownum += 1
                
    def clear_frameJSInner(self, controller):
        for widget in self.frameJSInner.winfo_children():
            widget.destroy()
    
    def combobox_changed(self, event, controller):
        #controller.special_js_config[fixname][propname] = str(self.comboboxes[propname].get())
        self.controller.js_gui_changed = 1
    
    def update_js_gui(self, controller):
        self.clear_frameJSInner(self.controller)
        self.create_frameJSInner(self.controller)
        #self.frameJS.reconfigure_autoscrollbar()      
        
    def returnframeJS(self):
        return self.frameJS
######

### Reset Functions
### ================================
def reset_all_tweaks(event, controller):
    #js_tweaker.setup_library(1)
    #js_tweaker.reset_html
    backend.clean_slate_css()
    manager.set_css_config_no_js(controller.css_config)
    #backend.reset_html()
    backend.clear_js_working_files()

def remake_js(event, controller):
    backend.clear_js_working_files()    
    thread = Thread(target = run_js_tweaker, args = (controller, 1,))
    thread.start()
    #thread.join()
    #run_js_tweaker(controller.frames["StartPage"].text1)

### Update Window
### ================================

class UpdateWindow(tk.Toplevel):
    def __init__(self, *args, **kwargs):
        self.controller = kwargs["controller"]
        
        ### Window, Title, Icon setup
        tk.Toplevel.__init__(self)
        self.container = custom_tk.ScrollFrame(self)
        windowW = 500
        windowH = 400
        screen_width = self.controller.winfo_screenwidth()
        screen_height = self.controller.winfo_screenheight()
        windowX = (screen_width / 2) - (windowW / 2)
        windowY = (screen_height / 2) - (windowH / 2) + 30
        self.geometry(f'{windowW}x{windowH}+{int(windowX)}+{int(windowY)}')
        self.wm_title("Small Update")
        add_window_icon(self)
        
        self.file_dates = kwargs["file_dates"]
        self.body = tk.Frame(self.container.content)

        self.defaultfont = self.controller.default_font.copy()
        self.smallfont = self.defaultfont.copy()
        self.smallfont.configure(size=12)
        
        self.messages = []
        self.labels = []
        
        self.prepop_update_window_text()
        total_rows = self.add_update_window_text()
        self.add_yes_no_frame(total_rows)
        
        self.body.grid(row=0, column=0, padx=10, sticky="n")
        self.container.pack(side="top", fill="both", expand=1)
        
    def prepop_update_window_text(self):
        #print(backend.format_file_dates_to_strings(self.file_dates))
        self.messages = backend.format_file_dates_to_strings(self.file_dates)

    def add_update_window_text(self):        
        for i, message in enumerate(self.messages):
            _labeltext = tk.StringVar()
            _labeltext.set(message)
            _label = tk.Label(self.body,
                              textvariable=_labeltext,
                              font=self.smallfont)
            #buttonr_tip = custom_tk.Detail_tooltip(label_a, "", hover_delay=200)
            _label.grid(row=i, column=0)
            self.labels.append(_label)
        return i
            
    def add_yes_no_frame(self, totalrows):
        ynFrame = tk.Frame(self.body)
        
        _labeltext = tk.StringVar()
        _labeltext.set("Update Files?")
        _label = tk.Label(ynFrame,
                          textvariable=_labeltext,
                          font=self.smallfont)
        #buttonr_tip = custom_tk.Detail_tooltip(label_a, "", hover_delay=200)
        _label.pack(padx=5)

        ybutton = ttk.Button(ynFrame,
                              text="Yes",
                              width=4
        )
        ybutton.bind("<Button-1>", lambda event:self.yes_update_click())
        ybutton.pack(pady=5)

        nbutton = ttk.Button(ynFrame,
                              text="No",
                              width=4
        )
        nbutton.bind("<Button-1>", lambda event:self.destroy())
        nbutton.pack(pady=(0,5)) 
        
        ynFrame.grid(row=0, column=1, padx=(20,0), rowspan=totalrows, sticky="e")

    def yes_update_click(self):
        files_list = backend.files_to_download_dtol(self.file_dates)
        backend.backup_old_versions(files_list)
        print("==============================")
        self.controller.frames["StartPage"].text1.update_idletasks()

        for filepath in files_list:
            #print("==============================")
            backend.download_file(filepath, backend.BRANCH)
            self.controller.frames["StartPage"].text1.update_idletasks()
        #Update LastPatchedDate
        backend.update_json_last_patched_date(self.controller.json_data)
        self.destroy()
        

### Settings Window
### ================================
def settings_window(event, controller):
    settings = tk.Toplevel(controller)
    windowW = 530
    windowH = 330
    screen_width = controller.winfo_screenwidth()
    screen_height = controller.winfo_screenheight()
    windowX = (screen_width / 2) - (windowW / 2) + 103
    windowY = (screen_height / 2) - (windowH / 2) + 30
    settings.geometry(f'{windowW}x{windowH}+{int(windowX)}+{int(windowY)}')
    settings.wm_title("Settings and About")
    
    add_window_icon(settings)
    settings.tkraise(controller)

    ### About Frame
    frameAbout = tk.Frame(settings)
        
    ###
    titlefont = controller.default_font.copy()
    titlefont.configure(size=16)
        
    labeltext_a = tk.StringVar()
    labeltext_a.set("SteamUI-OldGlory Installer (Release " + controller.release + ")")
    label_a = tk.Label(frameAbout, textvariable=labeltext_a, font=titlefont)
    buttonr_tip = custom_tk.Detail_tooltip(label_a, "GUI version " + controller.version, hover_delay=200)
    label_a.grid(row=0, column=0)

    ###
    subheadfont = titlefont.copy()
    subheadfont.configure(size=13)
    
    labeltext_b = tk.StringVar()
    labeltext_b.set("Created by Jonius7")
    label_b = tk.Label(frameAbout, textvariable=labeltext_b, font=subheadfont)
    label_b.grid(row=1, column=0, sticky="w", pady=(0,15))

    paragraphfont = titlefont.copy()
    paragraphfont.configure(size=10)

    ###
    about_text = tk.StringVar()

    bg = ttk.Style().lookup('TFrame', 'background')
    about = tk.Text(frameAbout,
                    font=paragraphfont,
                    bd=0,
                    bg=bg,
                    highlightthickness=0,
                    wrap='word',
                    width=70,
                    height=8)

    hyperlink = custom_tk.HyperlinkManager(about)
    
    about.insert(tk.END, "SteamUI-OldGlory is a set of tweaks that aim to improve the overall layout and appearance of the Steam Library, ")
    about.insert(tk.END, "and provide some extra functionality where possible.\n\n")
    about.insert(tk.END, 'Github: ')
    about.insert(tk.END, "github.com/Jonius7/SteamUI-OldGlory/", hyperlink.add(partial(webbrowser.open, "https://github.com/Jonius7/SteamUI-OldGlory/")))
    about.insert(tk.END, "\n\nTo be used with SteamFriendsPatcher:\n")
    about.insert(tk.END, "github.com/PhantomGamers/SteamFriendsPatcher/", hyperlink.add(partial(webbrowser.open, "https://github.com/PhantomGamers/SteamFriendsPatcher/")))

    about.config(state='disabled') 

    about.grid(row=2, column=0, sticky="w", pady=(0,15))
    
    
    

    
    ### Settings Frame
    frameGeneral = tk.Frame(settings)
    frameGeneral.grid_columnconfigure(0, weight=0)
    frameGeneral.grid_columnconfigure(1, weight=0)
    frameGeneral.grid_columnconfigure(2, weight=1)
    frameGeneral.grid_columnconfigure(3, weight=2)

    ###
    var_q = tk.IntVar()
    button_q = ttk.Button(frameGeneral,
                       text="Remake JS",
                       width=10
    )
    button_q.bind("<Button-1>", lambda event:remake_js(event, controller))
    buttonr_tip = custom_tk.Detail_tooltip(button_q, "Deletes libraryroot.beaut.js and reruns js_tweaker functions.\n" \
                                 "Most useful when something changes with a Steam Client Update", hover_delay=200)
    #buttonr_tip.add_image(open_img("images/full_layout.png"))
    button_q.grid(row=0, column=0, padx=5)

    ###
    var_r = tk.IntVar()
    button_r = ttk.Button(frameGeneral,
                       text="Reset",
                       width=10
    )
    button_r.bind("<Triple-Button-1>", lambda event:reset_all_tweaks(event, controller))
    buttonr_tip = custom_tk.Detail_tooltip(button_r, "WARNING!\n" \
                                 "Triple click this button to revert JS and CSS modifications.", hover_delay=200)
    button_r.grid(row=0, column=1, padx=5)

    ###
    var_s = tk.IntVar()
    button_s = ttk.Button(frameGeneral,
                       text="Check for Updates",
                       width=16
    )
    button_s.bind("<Button-1>", lambda event:start_update_check(event, controller))
    buttons_tip = custom_tk.Detail_tooltip(button_s, "Check for updates.\n" \
                                 "Small updates can be downloaded automatically.", hover_delay=200)
    button_s.grid(row=0, column=3, padx=5, sticky=tk.E)

    ###Pack Frames
    frameAbout.pack(fill="x", padx=10)
    frameGeneral.pack(fill="x", padx=10, pady=(0,30), side="bottom")


def start_update_check(event, controller):
    thread = Thread(target = controller.update_check, args = ())
    thread.start()
    
### ================================

def add_window_icon(window):
    icon_filename = 'steam_oldglory.ico'
    try:
        if OS_TYPE == "Windows":
            window.iconbitmap(resource_path(icon_filename))
        elif OS_TYPE == "Linux":
            icon = ImageTk.PhotoImage(file=icon_filename)   
            window.tk.call('wm', 'iconphoto', window._w, icon)
    except:
        print("Failed to load icon: " + icon_filename, file=sys.stderr)
        print_traceback()
        
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def print_traceback():
    print("~~~~~~~~~~~~~~~~~~~~")
    print(traceback.format_exc(), end='', file=sys.stderr)
    print("~~~~~~~~~~~~~~~~~~~~")

def main():
    app = OldGloryApp()
    app.mainloop()

if __name__ == "__main__":
    main()
