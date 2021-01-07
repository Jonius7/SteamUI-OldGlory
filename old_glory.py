import tkinter as tk
import tkinter.font as TkFont
from tkinter import ttk
from idlelib.tooltip import Hovertip, OnHoverTooltipBase, Message
from PIL import ImageTk, Image
import sys
import io
import backend
import js_tweaker
import os
import subprocess
import platform
import traceback
import requests
import webbrowser
from functools import partial
from tkHyperlinkManager import HyperlinkManager
#import queue
from threading import Thread

OS_TYPE = platform.system()
DEBUG_STDOUT_STDERR = False # Only useful for debugging purposes, set to True

class OldGloryApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        self.version = "v0.9.7 Beta"
        self.release = "5.1-pre"
      
        ### Window, Title, Icon setup
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        ### Fixed DPI Scaling on Windows
        if OS_TYPE == "Windows":
            #dpi = window.winfo_fpixels('1i')
            self.call('tk', 'scaling', 1.3)

        ### Window Dimensions/Position
        windowW = 760
        windowH = 660
        screen_width = container.winfo_screenwidth()
        screen_height = container.winfo_screenheight()
        windowX = (screen_width / 2) - (windowW / 2)
        windowY = (screen_height / 2) - (windowH / 2)
        self.geometry(f'{windowW}x{windowH}+{int(windowX)}+{int(windowY)}')
        self.minsize(width=windowW, height=windowH)
        self.maxsize(width=screen_width, height=screen_height)

        container.pack(side="top", fill="both", expand = True)

        ### Icon and Title
        add_window_icon(self)
        self.wm_title("SteamUI-OldGlory Configurer")        

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

        ### Grid configure
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        ### Load config variables
        self.js_gui_changed = 0
        
        ### Frames/Pages configure
        self.frames = {}
        
        for F in (StartPage, PageOne, PageTwo):
            frame = F(container, self)
            frame.grid(row=0, column=0, sticky="nsew")
            self.frames[F] = frame
        self.show_frame(StartPage)

    def show_frame(self, cont):
        self.frames[cont].tkraise()

    #init text log

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
    ### LOG FRAME
    ### Defined first even though it will be packed after the CHECK FRAME, due to redirecting StdOut
    ###
        frameLog = tk.Frame(self)

        ### Text
        entry1 = ttk.Entry(frameLog)
        self.text1 = tk.Text(entry1, height=12, width=92)
        self.text1.configure(font=("Arial",10))

        ### REDIRECT STDOUT STDERR
        if not DEBUG_STDOUT_STDERR:
            sys.stdout = StdoutRedirector(self.text1)
            sys.stderr = StderrRedirector(self.text1)
        
        self.text1.pack(expand="yes",fill="x")
        entry1.grid(row=0, column=0)

        ###
        scroll_1 = ttk.Scrollbar(frameLog, command=self.text1.yview)
        scroll_1.grid(row=0, column=1, sticky='ns')
        self.text1['yscrollcommand'] = scroll_1.set

        ### load JSON
        controller.json_data = backend.get_json_data()


    ### HEAD FRAME
    ###
        self.frameHead = head_frame(self, controller)

    ### Tabs
        tabs = ttk.Notebook(self,)
        frameCheck = tk.Frame(tabs)
        framePatch = tk.Frame(tabs)
    
    ### CHECK FRAME
    ###
        
        #frameCheck.grid_columnconfigure(2, weight=1)

        ######
        self.var1 = tk.IntVar()
        check1 = ttk.Checkbutton(frameCheck,
                                 variable=self.var1
                                 )                        
        check1.bind("<Button-1>", lambda event:css_cb_check(event, self.var1, [check2, check3, check5]))
        check1.grid(row=0, column=0)
        ###        
        mo1 = MainOption(
            parentFrame=frameCheck,
            page=self,
            name="Install CSS Tweaks",
            image="images/full_layout.png",
            tags=["CSS"])
        mainoption1 = mo1.returnMainOption()
        mainoption1.grid(row=0, column=1, sticky='w')
        
        ######
        self.var2 = tk.IntVar()
        check2 = ttk.Checkbutton(frameCheck,
                                 variable=self.var2,
                                 state='disabled')
        check2.grid(row=1, column=0)
        ###
        mo2 = MainOption(
            parentFrame=frameCheck,
            page=self,
            name="  \u2937 Box Play Button",
            image="images/play_button_box.png",
            tags=["CSS"])
        mainoption2 = mo2.returnMainOption()
        mainoption2.grid(row=1, column=1, sticky='w')

        
        ######
        self.var3 = tk.IntVar()
        check3 = ttk.Checkbutton(frameCheck,
                                 variable=self.var3,
                                 state='disabled')
        check3.bind("<Button-1>", lambda event:css_cb_check(event, self.var3, [check4]))
        check3.grid(row=2, column=0)
        ###
        mo3 = MainOption(
            parentFrame=frameCheck,
            page=self,
            name="  \u2937 Vertical Nav Bar",
            image="images/vertical_nav_bar.png",
            tags=["CSS", "JS"])
        mainoption3 = mo3.returnMainOption()
        mainoption3.grid(row=2, column=1, sticky='w')
        
        
        ######
        self.var4 = tk.IntVar()
        check4 = ttk.Checkbutton(frameCheck,
                                 variable=self.var4,
                                 state='disabled'
                                 )
        check4.grid(row=3, column=0)
        ###
        mo4 = MainOption(
            parentFrame=frameCheck,
            page=self,
            name="    \u2937 Classic Layout",
            image="images/classic_layout.png",
            tags=["CSS", "JS"])
        mainoption4 = mo4.returnMainOption()
        mainoption4.grid(row=3, column=1, sticky='w')
        
        ######
        self.var5 = tk.IntVar()
        check5 = ttk.Checkbutton(frameCheck,
                                 variable=self.var5)
        check5.grid(row=4, column=0)
        ###
        mo5 = MainOption(
            parentFrame=frameCheck,
            page=self,
            name="  \u2937 Landscape Game Images",
            image="images/landscape_images.png",
            tags=["CSS", "JS"])
        mainoption5 = mo5.returnMainOption()
        mainoption5.grid(row=4, column=1, sticky='w')

        ######
        self.change_theme = 0
        self.var6 = tk.IntVar()
        check6 = ttk.Checkbutton(frameCheck,
                                 variable=self.var6)
        check6.bind("<Button-1>", lambda event: self.setChangeTheme(event))
        check6.grid(row=5, column=0)
        ###
        mo6 = MainOption(
            parentFrame=frameCheck,
            page=self,
            name="Library Theme",
            image="images/theme_shiina.png",
            tags=["CSS"])
        mainoption6 = mo6.returnMainOption()
        mainoption6.grid(row=5, column=1, sticky='w')
        ###
        self.dropdown6_value = tk.StringVar()
        self.dropdown6 = ttk.Combobox(frameCheck,
                                 font="TkDefaultFont",
                                 values=self.getListOfThemeNames(controller),
                                 state="readonly",
                                 textvariable=self.dropdown6_value,
                                 width=30)
        self.dropdown6.current(0)
        self.dropdown6.bind("<<ComboboxSelected>>", lambda event: dropdown_click(event, self, controller))
        self.dropdown6.grid(row=6, column=1, columnspan=2, sticky="w")
        
        
        ###
        label_end = tk.Label(frameCheck, height=0)
        label_end.grid(row=7, column=0, columnspan=2)

        ###
        self.image1 = add_img(frameCheck, resource_path('images/full_layout.png'))
        self.image1.grid(row=0, column=4, rowspan=8, padx=5, sticky="n")      

    ### PATCH FRAME
    ###
        labeltext_a = tk.StringVar()
        labeltext_a.set("Nothing much here... yet")
        
        label_a = tk.Label(framePatch, textvariable=labeltext_a)
        label_a.grid(row=0, column=0)


    ### MODE FRAME
    ###
        frameMode = tk.Frame(self)

        ###
        self.var_m = tk.IntVar()
        button_m = ttk.Button(frameMode,
                           text="CSS Options",
                           width=16
        )
        button_m.bind("<Button-1>", lambda event:show_PageOne(controller))
        button_m.grid(row=0, column=0, padx=5)

        ###
        self.var_n = tk.IntVar()
        button_n = ttk.Button(frameMode,
                           text="JS Options",
                           width=16
        )
        button_n.bind("<Button-1>", lambda event:show_PageTwo(controller))
        button_n.grid(row=0, column=1, padx=5)

        
    ### CONFIRM FRAME
    ###
        frameConfirm = confirm_frame(self, controller)


        ### Running functions after much of StartPage has been initialised
        ### Check if CSS Patched
        ### Check for new version
        self.text1.config(state='normal')
        check_if_css_patched(self)
        update_check(self, controller.release)
        
        ### Set GUI from config
        self.loaded_config = set_selected_from_config(self, controller)
        self.text1.config(state='disabled')
        init_cb_check(self.var1, [check2, check3, check5])
        init_cb_check(self.var3, [check4])        
        
    ### Pack frames
    ###
        self.frameHead.pack()
        frameCheck.pack()
        framePatch.pack()

        ###tabs
        tabs.add(frameCheck, text="Main Options")
        tabs.add(framePatch, text="Advanced Options")
        tabs.pack(expand=1)
        
        frameLog.pack(pady=(10,7))
        frameConfirm.pack(pady=(7, 20), side="bottom", fill="x")
        frameMode.pack(pady=(2, 0), side="bottom")

    ### Getters
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

class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

    ### HEAD FRAME
    ###
        self.frameHead = head_frame(self, controller)

    ### Tabs
        tabs = ttk.Notebook(self,)
        frameQuick = tk.Frame(tabs)
        frameModules = tk.Frame(tabs)

    ### CSS Frame
    ###
        controller.css_config = backend.load_css_configurables()
        self.frameCSS = tk.Frame(self)
        self.css_gui = CSSGUICreator(self, controller, controller.css_config)
        self.frameCSS = self.css_gui.returnframeCSS()
        
    ### MODE Frame
    ###
        frameMode = tk.Frame(self)

        ###
        self.var_m = tk.IntVar()
        button_m = ttk.Button(frameMode,
                           text="Back to Home",
                           width=16
        )
        button_m.bind("<Button-1>", lambda event:controller.show_frame(StartPage))
        button_m.grid(row=0, column=0, padx=5)

        ###
        self.var_n = tk.IntVar()
        button_n = ttk.Button(frameMode,
                           text="JS Options",
                           width=16
        )
        button_n.bind("<Button-1>", lambda event:show_PageTwo(controller))
        button_n.grid(row=0, column=1, padx=5)

    ### CONFIRM FRAME
    ###
        frameConfirm = confirm_frame(self, controller)
        
    ### Pack frames
        self.frameHead.pack()
        self.frameCSS.pack(padx=10, fill="x")
        frameConfirm.pack(pady=(7, 20), side="bottom", fill="x")
        frameMode.pack(pady=(2, 0), side="bottom")

        #self.frameCSS = create_css_gui(self, controller, backend.load_css_configurables())

class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

    ### HEAD FRAME
    ###
        self.frameHead = head_frame(self, controller)

    ### JS FRAME
    ###
        controller.js_config, controller.special_js_config = backend.load_js_fixes()
        self.frameJS = tk.Frame(self)
        self.js_gui = JSFrame(self, controller)
        self.frameJS = self.js_gui.returnframeJS()
        
    ### MODE Frame
    ###
        frameMode = tk.Frame(self)

        ###
        self.var_m = tk.IntVar()
        button_m = ttk.Button(frameMode,
                           text="Back to Home",
                           width=16
        )
        button_m.bind("<Button-1>", lambda event:controller.show_frame(StartPage))
        button_m.grid(row=0, column=0, padx=5)

        ###
        self.var_n = tk.IntVar()
        button_n = ttk.Button(frameMode,
                           text="CSS Options",
                           width=16
        )
        button_n.bind("<Button-1>", lambda event:show_PageOne(controller))
        button_n.grid(row=0, column=1, padx=5)

    ### CONFIRM FRAME
    ###
        frameConfirm = confirm_frame(self, controller)

    ### Pack frames
    ###
        self.frameHead.pack()
        self.frameJS.pack()
        frameConfirm.pack(pady=(7, 20), side="bottom", fill="x")
        frameMode.pack(pady=(2, 0), side="bottom")

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
def confirm_frame(page, controller):
    frameConfirm = tk.Frame(page)
    
    frameConfirm.grid_columnconfigure(0, weight=1)
    frameConfirm.grid_columnconfigure(1, weight=0)
    frameConfirm.grid_columnconfigure(2, weight=0)
    frameConfirm.grid_columnconfigure(3, weight=1)

    ###
    label_left = tk.Label(frameConfirm, width=3)
    label_left.grid(row=0, column=0, padx=(5,14))
    
    ###
    button1 = ttk.Button(frameConfirm,
                       text="Install",
                       width=15                       
    )
    button1.bind("<Button-1>",
                 lambda event:globals()["install_click"](event, controller.frames[StartPage], controller)
                 )
    button1.grid(row=0, column=1, padx=5, sticky="NSEW")
    
    ###
    button2 = ttk.Button(frameConfirm,
                       text="Reload Config",
                       width=15#,
                       ###state='disabled'
    )
    button2_tip = Detail_tooltip(button2, "If you have modified the files manually,\nclick here to reload their values into the program.", hover_delay=200)
    button2.bind("<Button-1>",
                 lambda event:reload_click(event, controller)
                 )
    button2.grid(row=0, column=2, padx=5, sticky="NSEW")

    ###
    settings_image = open_img(globals()["resource_path"]('images/settings.png'), 24)
    button3 = ttk.Button(frameConfirm,
                       #text="GG",
                       image=settings_image,
                       width=3#,
                       ###state='disabled'
    )
    button3.image = settings_image
    button3_tip = Detail_tooltip(button3, "Settings and About", hover_delay=200)
    button3.bind("<Button-1>",
                 lambda event:settings_window(event, controller)
                 )
    button3.grid(row=0, column=3, padx=(5,15), sticky=tk.E)
    
    return frameConfirm
### ================================

### Show Page Functions
### ================================
def show_PageOne(controller):
    #controller.css_config = backend.load_css_configurables()
    controller.show_frame(PageOne)
    #controller.frames[PageOne].frameCSS = create_css_gui(controller.frames[PageOne], controller, backend.load_css_configurables())
    #update_css_gui(controller.frames[PageOne], controller, controller.css_config)
def show_PageTwo(controller):
    #controller.js_config = backend.load_js_fixes()
    controller.show_frame(PageTwo)

### ================================
### Initialisation
### ================================
### Check SteamFriendsPatcher
def check_if_css_patched(page):
    if not backend.is_css_patched():
        hyperlink = HyperlinkManager(page.text1)
        page.text1.tag_configure("err", foreground="red")
        page.text1.insert(tk.END, '==============================\n')
        page.text1.insert(tk.INSERT, "css/5.css (previously known as libraryroot.css) not patched.\n", ("err"))
        page.text1.insert(tk.INSERT, "Download ")
        page.text1.insert(tk.INSERT, "SteamFriendsPatcher\n", hyperlink.add(partial(webbrowser.open, "https://github.com/PhantomGamers/SteamFriendsPatcher/")))
        page.text1.insert(tk.INSERT, "\n")

### Check if newer version
def update_check(page, current_release):
    try:
        response = requests.get("https://api.github.com/repos/jonius7/steamui-oldglory/releases/latest", timeout=0.5)
        latest_release = response.json()["name"]
        if latest_release == current_release:
            print("You are up to date. Release " + latest_release + "\n")
        else:
            hyperlink = HyperlinkManager(page.text1)
            page.text1.insert(tk.END, 'New version available: ')
            page.text1.insert(tk.END, "Release {0}\n".format(latest_release), hyperlink.add(partial(webbrowser.open, "https://github.com/Jonius7/SteamUI-OldGlory/releases/latest")))
            page.text1.insert(tk.END, 'Current version: ')
            page.text1.insert(tk.END, "Release {0}\n".format(current_release))
            page.text1.insert(tk.INSERT, "\n")
    except requests.exceptions.ConnectionError:
        print("Could not connect to Github, Unable to check for latest release!", file=sys.stderr)
    except:
        print("Unable to check for latest release!", file=sys.stderr)
        print_traceback()
    
### StartPage
### Select checkboxes based on config
def set_selected_from_config(page, controller):
    ### grab stdout, stderr from function in backend
    f = io.StringIO()
    loaded_config = backend.load_config()
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
### ================================
   

### Redirect Stdout, Stderr
### ================================
class IORedirector(object):
    def __init__(self, text_area):
        self.text_area = text_area

class StdoutRedirector(IORedirector):
    def write(self, text):
        self.text_area.config(state='normal')
        self.text_area.config(foreground="black")
        self.text_area.insert(tk.END, text)
        self.text_area.yview_pickplace("end")
        self.text_area.config(state='disabled')        
    def flush(self):
        pass

class StderrRedirector(IORedirector):
    def write(self, text):
        self.text_area.config(state='normal')
        self.text_area.tag_configure("err", foreground="red")
        self.text_area.insert(tk.END, text, ("err"))
        self.text_area.yview_pickplace("end")
        self.text_area.config(state='disabled')        
    def flush(self):
        pass
### ================================

### Checkbox Validation - Disable
### ================================
### still the two functions, instead of 1, probably due to init
def css_cb_check(event, var1, checks):
    if var1.get() == 0:
        for check in checks:
            check.config(state='enabled')
    else:
        for check in checks:
            check.config(state='disabled')
        
def init_cb_check(var1, checks):
    if var1.get() == 1:
        for check in checks:
            check.config(state='enabled')
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
        self.label.bind("<Button-1>", lambda event: globals()["change_image"](self.page.image1, globals()["resource_path"](self.image)))
        self.label.grid(row=0, column=0, sticky='w')

        for i, tagName in enumerate(kwargs["tags"], start=1):
            leftPadding = (5, 0) if i == 1 else 0
            tag = add_img(self.tagFrame, globals()["resource_path"]('images/tag_'+tagName+'.png'), width=50)
            tag.grid(row=0, column=i, sticky='w', padx=leftPadding)
            self.tags[self.name]=tag
    def returnMainOption(self):
        return self.tagFrame

### Dropdown click (theme)
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
    theme_image_path = resource_path("images/theme_" + controller.json_data["themes"][theme_name.split(" (")[0]]["filename"][1:-5] + ".png")
    if os.path.isfile(theme_image_path):
        #change_image
        change_image(page.image1, theme_image_path)
    else:
        change_image(page.image1, resource_path("images/no_preview.png"))
        
### INSTALL Functions
### ================================
### Map config values to selected checkboxes
CONFIG_MAP = {"SteamLibraryPath" : {"set" : ""},
              "PatcherPath" : {"set" : ""},
              "" : {},
              "InstallCSSTweaks" : {"value" : "var1", "javascript" : False},
              "EnablePlayButtonBox" : {"value" : "var2", "javascript" : False},
              "EnableVerticalNavBar" : {"value" : "var3", "javascript" : True},
              "EnableClassicLayout" : {"value" : "var4", "javascript" : True},
              "LandscapeImages" : {"value" : "var5", "javascript" : True},
              "InstallWithDarkLibrary" : {"value" : "var6", "javascript" : False},
              "ThemeSelected" : {"set" : ""}
              }



### Install Click
def install_click(event, page, controller):
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

### Get settings to apply (with validation), and values
### some of this needs to be changed to account for "unchecking" options
def get_settings_from_gui(event, page):
    try:
        settings = []
        settings_values = {}
        for key in CONFIG_MAP:
            if "value" in CONFIG_MAP[key]:         
                settings_values[key] = page.getCheckbuttonVal(CONFIG_MAP[key]["value"]).get()
                if page.getCheckbuttonVal(CONFIG_MAP[key]["value"]).get() == 1:
                    settings.append(key)
                elif page.getCheckbuttonVal(CONFIG_MAP[key]["value"]).get() != int(page.loaded_config[key]):
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
        print("libraryroot.custom.css not found", file=sys.stderr)
        print_traceback()

# Rather not have this as hard coded as it currently is
def apply_changes_to_config(controller, settings_values):
    #print(settings_values.keys())
    if "EnableVerticalNavBar" in settings_values.keys():
        controller.js_config["Vertical Nav Bar (beta, working)"] = str(settings_values["EnableVerticalNavBar"])
        controller.frames[PageTwo].js_gui.checkvars["Vertical Nav Bar (beta, working)"].set(settings_values["EnableVerticalNavBar"])
    if "EnableClassicLayout" in settings_values.keys():
        if settings_values["EnableClassicLayout"] == 1 and settings_values["EnableVerticalNavBar"] == 0:
            settings_values["EnableClassicLayout"] = 0        
    if "LandscapeImages" in settings_values.keys():
        controller.js_config["Landscape Images JS Tweaks (beta, working, some layout quirks with shelves)"] = str(settings_values["LandscapeImages"])
        controller.frames[PageTwo].js_gui.checkvars["Landscape Images JS Tweaks (beta, working, some layout quirks with shelves)"].set(settings_values["LandscapeImages"])
    for key in controller.special_js_config:
        if "Change Game Image Grid Sizes" in key:
            sizes = ["Small", "Medium", "Large"]
            for size in sizes:
                controller.special_js_config[key][size] = controller.frames[PageTwo].js_gui.comboboxes[size].get()
    return settings_values
    #print(controller.special_js_config)

### Write CSS settings (comment out sections) + run js_tweaker if needed
def apply_settings_from_gui(page, controller, settings_to_apply, settings_values):

    ### Check if js required
    change_javascript = 0
    for setting in settings_values:
        #print("javascript" in CONFIG_MAP[setting])
        if "javascript" in CONFIG_MAP[setting]:
            if CONFIG_MAP[setting]["javascript"] \
            and int(page.loaded_config[setting]) != page.getCheckbuttonVal(CONFIG_MAP[setting]["value"]).get():
                #print(int(page.loaded_config[setting]))
                #print(page.getCheckbuttonVal(CONFIG_MAP[setting]["value"]).get())
                css_config_js_enabled(controller.css_config)
                change_javascript = 1
    if controller.js_gui_changed == 1:
        css_config_js_enabled(controller.css_config)
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

   
def run_js_tweaker(text_area):
    try:
        print("==============================")
        print("Running js_tweaker")
        text_area.update_idletasks()

        ###
        js_tweaker.initialise()
        js_tweaker.copy_files_from_steam()
        text_area.update_idletasks()
        js_tweaker.beautify_js()
        text_area.update_idletasks()
        js_tweaker.setup_library()
        text_area.update_idletasks()
        js_tweaker.parse_fixes_file("fixes.txt")
        text_area.update_idletasks()
        js_tweaker.write_modif_file()
        #text_area.update_idletasks()
        js_tweaker.re_minify_file()
        text_area.update_idletasks()
        js_tweaker.copy_files_to_steam()
        text_area.update_idletasks()
        print("\nSteam Library JS Tweaks applied successfully.")
              
    except Exception as e:
        print(e, file=sys.stderr)

#need rewrite
def apply_css_theme(page, controller):
    '''
    if page.var6.get() == 1:
        theme_name = page.dropdown6.get()
        print("Applying CSS Theme: " + theme_name)
        backend.apply_css_theme(THEME_MAP[theme_name]["filename"],
                            THEME_MAP[theme_name]["order"],
                            THEME_MAP[theme_name]["patchtext"])
        page.text1.update_idletasks()
    elif page.var6.get() == 0 and page.change_theme == 1:
        backend.remove_current_css_themes("no_themes.css", "before")
        page.text1.update_idletasks()
        print("Cleared current CSS Themes")
    page.change_theme = 0
    '''

    if page.var6.get() == 1:
        theme_full_name = page.dropdown6.get()
        print("Applying CSS Theme: " + theme_full_name)
        theme_name = theme_full_name.split(" (")[0]
        #print(controller.json_data["themes"][theme_name]["filename"])
        backend.enable_css_theme(controller.json_data["themes"][theme_name]["filename"],
                         controller.json_data["themes"][theme_name]["order"],
                         controller.json_data)
    elif page.var6.get() == 0 and page.change_theme == 1:
        backend.enable_css_theme("none", "after", controller.json_data)
    page.change_theme = 0    
                                
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

### ================================


### RELOAD Functions
### ================================
def reload_click(event, controller):
    try:
        print("==============================")
        controller.css_config = backend.load_css_configurables()
        controller.js_config, controller.special_js_config = backend.load_js_fixes()
        controller.frames[PageTwo].js_gui.update_js_gui(controller)
        controller.frames[PageOne].css_gui.PresetFrame.set_preset_default()
        print("Config Reloaded.")
    except:
        print("Config could not be completely reloaded.", file=sys.stderr)
### ================================


### Image Functions
### ================================
def open_img(filename, width=350):
    try:
        x = filename
        img = Image.open(x)
        new_width = width
        new_height = int(new_width * img.height / img.width)
        img = img.resize((new_width, new_height), Image.ANTIALIAS)
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

### Tooltip
### ================================
class Detail_tooltip(OnHoverTooltipBase):
    def __init__(self, anchor_widget, text, hover_delay=1000):
        super(Detail_tooltip, self).__init__(anchor_widget, hover_delay=hover_delay)
        self.text = text
        
    def showcontents(self):
        message = Message(self.tipwindow, text=self.text, justify='left',
                      background="#ffffe0", width=590, relief='solid', borderwidth=1)
        message.pack()
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
        self.frameCSS = tk.Frame(page)
        #x = ConfigurablesFrame(self.frameCSS, controller, config)
        #self.frameConfigurables = x.returnFrame()
        #self.labels = x.returnCSSFrame().returnLabels()
        #self.entryboxes = x.returnCSSFrame().returnEntryboxes()
        #for label in x.returnLabels():
        #    print(label["text"])
        self.PresetFrame = PresetFrame(self.frameCSS, controller, config)
        self.framePreset = self.PresetFrame.returnPresetFrame()

        #Configure grid expand
        self.frameCSS.columnconfigure(0, weight=2)
        self.frameCSS.rowconfigure(0, weight=1)
        self.frameCSS.columnconfigure(1, weight=1)
        
        self.framePreset.grid(row=0, column=0, sticky="nsew")
        #self.frameConfigurables.grid(row=0, column=1, sticky="nsew")
        #frameConfigurables.pack(fill="both", expand=True, padx=10)
    def returnframeCSS(self):
        return self.frameCSS
    #def returnframeConfigurables(self):
    #    return self.frameConfigurables  
    #def returnCSSGUI(self):
    #    return self

### START ConfigurablesFrame
###
# Currently unused
class ConfigurablesFrame(tk.Frame):
    def __init__(self, parent, controller, config):
        self.parent = parent
        self.frameConfigurables = tk.Frame(self.parent)
        self.controller = controller
        self.config = config

        ###
        self.frameConfigurables = tk.Frame(self.parent)
    
        canvasCSS = tk.Canvas(self.frameConfigurables, highlightthickness=0, yscrollincrement=10) #remove highlight black border wtf
        canvasCSS.pack(side="left")
        #canvasCSS.grid(row=0, column=0, padx=10, sticky="nsew")
        

        ### Scrollbar
        scroll_1 = ttk.Scrollbar(self.frameConfigurables, command=canvasCSS.yview)
        scroll_1.pack(side="right", fill="y")
        #scroll_1.grid(row=0, column=1, sticky="nsew")
        canvasCSS.configure(yscrollcommand=scroll_1.set)
        canvasCSS.bind('<Configure>', lambda e: canvasCSS.configure(scrollregion = canvasCSS.bbox('all')))
        
        ### Inner frame
        self.frameCSS = tk.Frame(canvasCSS)
        canvasCSS.create_window((0,0), window=self.frameCSS, anchor="nw")
        canvasCSS.pack(fill=BOTH, expand=YES)
        
        ### Section title font
        sectionfont = self.controller.default_font.copy()
        sectionfont.configure(underline=1)

        ### Populate config
        row = -1
        self.labels = []
        self.entryboxes = {}
        
        for i, section in enumerate(self.config):
            row += 1
            self.label = tk.Label(self.frameCSS,
                              text=section,
                             font=sectionfont,
                             fg='blue')
            self.label.grid(row=row, column=0)
            self.labels.append(self.label)
            
            for j, prop in enumerate(self.config[section]):
                #print(config[section][prop]['options'])
                self.propDict = self.config[section][prop]
                obj = CSSConfigRow(prop, self.propDict, self.frameCSS)
                frameCSSSection = obj.returnCSSConfigRow()
                row += 1
                frameCSSSection.grid(row=row, column=0, padx=(15, 0))
                #self.configRows.append(frameCSSSection)
                self.entryboxes[obj.label["text"]] = obj.combobox
    def returnFrame(self):
        return self.frameConfigurables
    def returnLabels(self):
        return self.labels
    def returnEntryboxes(self):
        return self.entryboxes
    def returnCSSFrame(self):
        return self        

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
            tip = Detail_tooltip(self.label, formatted_hover_text(self.propDict['default'], self.propDict['desc']), hover_delay=200)
            
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
                    "Custom value" : {"value" : "4"}
                    }


### START PresetFrame
class PresetFrame(tk.Frame):
    def __init__(self, parent, controller, config):
        self.parent = parent
        self.framePreset = tk.Frame(self.parent)
        self.controller = controller
        self.config = config #unused?
            
        label_preset_head = tk.Label(self.framePreset, text="Quick CSS Options (more coming soon)")
        label_preset_head.grid(row=0, column=0)


    def getPresetOptions(self):
        print("TODO")
        try:
            if "quickCSS" in self.controller.json_data:
                print("quickCSS found")
            else:
                print("ERROR")
        except:
            print_traceback()
        
        
                
        
    
    ### PRESET Click funtion
    def preset_click(self, controller, radioText):
        #print("~~~pcccc~~~~~~")
        #print(radioText)
        if radioText != "Custom value":
            globals()["apply_css_config_values"](controller, self.radios_config[radioText]["config"])
        #print(controller.css_config)

    
    ###    
    def returnPresetFrame(self):
        return self.framePreset

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
### END PresetFrame


### START PresetOption

def PresetOption(self, parent, controller, optiondata):

    def __init__(self, parent, controller, config):
    ###
        self.preset_title = tk.Label(self.framePreset, text="What's New")
        self.preset_title.grid(row=1, column=0, padx=(5,0))


        
        self.radios_config = {"Top of Page" : {"value" : "1", "config" :
                            {"--WhatsNew" : "block",
                            "--WhatsNewOrder" : "0"}},
                              "Bottom of page" : {"value" : "2", "config" : 
                            {"--WhatsNew" : "block",
                            "--WhatsNewOrder" : "2"}},
                  "Hide entirely" : {"value" : "3", "config" :
                            {"--WhatsNew" : "none",
                            "--WhatsNewOrder" : "0"}},
                    "Custom value" : {"value" : "4"}
                  }
        self.radiovar = tk.StringVar()
        #self.radiovar.set("2")
        self.set_preset_default()
        self.radios = []
        
        for i, (textv, value) in enumerate(self.radios_config.items(), 1):
            _radio = ttk.Radiobutton(self.framePreset,
                            text = textv, 
                            variable = self.radiovar,
                            value = value["value"],
                            command = lambda textv = textv: self.preset_click(controller, textv)
                            )
            _radio.grid(row=i+1, column=0, padx=(5,0), sticky='w')
            self.radios.append(_radio)


    ### set selected based on value in css_config
    def set_preset_default(self):
        #print(self.controller.css_config)
        key_set = 0
        for key in self.radios_config:
            equal = False
            if "config" in self.radios_config[key]:
                equal = True
                for prop in self.radios_config[key]["config"]:
                    #print(prop)
                    #print("KEY : VALUE")
                    
                    #if value in self.radios_config matches value in css_config
                    equal = (self.radios_config[key]["config"][prop] == get_item(prop, self.controller.css_config)) and equal
                    #print((self.radios_config[key]["config"][prop] == get_item(prop, self.controller.css_config)))
                    #print(self.radios_config[key]["config"][prop])
                    #print(get_item(prop, self.controller.css_config))
                    ##print(prop + " : " + get_item(prop, self.controller.css_config))
            #print(key + " | " + str(equal))
            if equal:
                self.radiovar.set(self.radios_config[key]["value"])
                key_set = 1
        if key_set == 0:
            self.radiovar.set(self.radios_config["Custom value"]["value"])




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
        self.frameJS = tk.Frame(page)
        self.controller = controller
        self.frameJSInner = tk.Frame(self.frameJS)
            
        label_js_head = tk.Label(self.frameJSInner, text="JS Options")
        label_js_head.grid(row=0, column=0, columnspan=2)

        self.checkvars = {}
        self.comboboxes = {}
        self.create_frameJSInner(self.controller)
        self.frameJSInner.pack()
        
    ### PRESET Click funtion
    def js_click(self, controller, fixname):
        try:
            controller.js_config[fixname] = str(self.checkvars[fixname].get())
            self.controller.js_gui_changed = 1
            #print(controller.js_config)
        except Exception as e:
            print("Error setting config :\n"\
                  "Fix:   " + fixname +\
                  "Value: " + str(value), file=sys.stderr)
            
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
            #_label.bind("<Button-1>", lambda event: globals()["change_image"](self.page.image1, globals()["resource_path"](self.image)))

            _checkbutton.grid(row=rownum, column=0, padx=(5,0), sticky='w')
            _label.grid(row=rownum, column=1, sticky='w')
            
            
            rownum += 1
            if fixname in self.controller.special_js_config:
                #print(self.controller.special_js_config["Change Game Image Grid Sizes (optional) - default widths 111, 148, 222"])
                self.sizesFrame = tk.Frame(self.frameJSInner)
                special_js_key_name = "Change Game Image Grid Sizes (optional) - default widths 111, 148, 222"
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
        #for checkvar in self.checkvars:
            #print(checkvar.get())
        
    def returnframeJS(self):
        return self.frameJS
######

### Reset Functions
### ================================
def reset_all_tweaks(event, controller):
    js_tweaker.setup_library(1)
    backend.clean_slate_css()
    css_config_reset(controller.css_config)
    #backend.reset_html()
    backend.clear_js_working_files()

def remake_js(event, controller):
    backend.clear_js_working_files()    
    
    thread = Thread(target = run_js_tweaker, args = (controller.frames[StartPage].text1, ))
    thread.start()
    #thread.join()
    #run_js_tweaker(controller.frames[StartPage].text1)


### Set some CSS values back to "default"
### ================================
### Mainly HoverPosition
def css_config_reset(css_config):
    css_config["Left Sidebar - Games List"]["--HoverOverlayPosition"]["current"] = "0"
    return css_config

def css_config_js_enabled(css_config):
    css_config["Left Sidebar - Games List"]["--HoverOverlayPosition"]["current"] = "unset"
    return css_config

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
    labeltext_a.set("SteamUI-OldGlory Configurer (Release " + controller.release + ")")
    label_a = tk.Label(frameAbout, textvariable=labeltext_a, font=titlefont)
    buttonr_tip = Detail_tooltip(label_a, "GUI version " + controller.version, hover_delay=200)
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

    hyperlink = HyperlinkManager(about)
    
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


    ###
    var_q = tk.IntVar()
    button_q = ttk.Button(frameGeneral,
                       text="Remake JS",
                       width=10
    )
    button_q.bind("<Button-1>", lambda event:remake_js(event, controller))
    buttonr_tip = Detail_tooltip(button_q, "Deletes libraryroot.beaut.js and reruns js_tweaker functions.\n" \
                                 "Most useful when something changes with a Steam Client Update", hover_delay=200)
    button_q.grid(row=0, column=0, padx=5)

    ###
    var_r = tk.IntVar()
    button_r = ttk.Button(frameGeneral,
                       text="Reset",
                       width=10
    )
    button_r.bind("<Triple-Button-1>", lambda event:reset_all_tweaks(event, controller))
    buttonr_tip = Detail_tooltip(button_r, "WARNING!\n" \
                                 "Triple click this button to revert JS and CSS modifications.", hover_delay=200)
    button_r.grid(row=0, column=1, padx=5)

    ###Pack Frames
    frameAbout.pack(fill="x", padx=10)
    frameGeneral.pack(fill="x", padx=10, pady=(0,30), side="bottom")
    
    
### ================================

def add_window_icon(window):
    icon_filename = 'steam_oldglory.ico'
    try:
        if OS_TYPE == "Windows":
            window.iconbitmap(resource_path(icon_filename))
        elif OS_TYPE == "Linux":
            icon = PhotoImage(file=icon_filename)   
            root.tk.call('wm', 'iconphoto', root._w, icon)
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
