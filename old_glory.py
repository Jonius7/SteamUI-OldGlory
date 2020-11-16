import tkinter as tk
import tkinter.font as TkFont
from tkinter import ttk
from idlelib.tooltip import *
from PIL import ImageTk, Image
import sys
import io
import backend
import js_tweaker
import os
import subprocess
import platform
import traceback
#import queue
#from threading import Thread

OS_TYPE = platform.system()
DEBUG_STDOUT_STDERR = False  # Only useful for debugging purposes, set to True


class OldGloryApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        ### Window, Title, Icon setup
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        windowW = 740
        windowH = 620
        self.geometry((str(windowW)+'x'+str(windowH)+'+650+300'))
        self.minsize(width=windowW, height=windowH)
        self.maxsize(width=windowW, height=windowH)
        container.pack(side="top", fill="both", expand = True)
        
        if OS_TYPE == "Windows":
            self.iconbitmap(resource_path('steam_oldglory.ico'))
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
        
        ### Styling Combobox dropdown
        self.option_add("*TCombobox*Listbox*font", (self.default_font))
        
        '''
        style.configure("TRadiobutton",
                highlightthickness=0,
                borderwidth=0,
                relief=SOLID,
                indicatoron=False,)
        '''

        ### Grid configure
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        ### Loaded CSS Configurables
        self.css_config = backend.load_css_configurables()
        
        ### Frames/Pages configure
        self.frames = {}
        
        for F in (StartPage, PageOne, PageTwo):
            frame = F(container, self)
            frame.grid(row=0, column=0, sticky="nsew")
            self.frames[F] = frame
        self.show_frame(StartPage)

    def show_frame(self, cont):
        self.frames[cont].tkraise()

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)           

    ### HEAD FRAME
    ###
        self.frameHead = head_frame(self, controller)

    ### CHECK FRAME
    ###
        frameCheck = tk.Frame(self)
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
            image="full_layout.png",
            tags=["CSS"])
        mainoption1 = mo1.returnMainOption()
        mainoption1.grid(row=0, column=1, sticky=W)
        
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
            image="play_button_box.png",
            tags=["CSS"])
        mainoption2 = mo2.returnMainOption()
        mainoption2.grid(row=1, column=1, sticky=W)

        
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
            image="vertical_nav_bar.png",
            tags=["CSS", "JS"])
        mainoption3 = mo3.returnMainOption()
        mainoption3.grid(row=2, column=1, sticky=W)
        
        
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
            image="classic_layout.png",
            tags=["CSS", "JS"])
        mainoption4 = mo4.returnMainOption()
        mainoption4.grid(row=3, column=1, sticky=W)
        
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
            image="landscape_images.png",
            tags=["CSS", "JS"])
        mainoption5 = mo5.returnMainOption()
        mainoption5.grid(row=4, column=1, sticky=W)

        ######
        self.var6 = tk.IntVar()
        check6 = ttk.Checkbutton(frameCheck,
                                 variable=self.var6)
        check6.grid(row=5, column=0)
        ###
        mo6 = MainOption(
            parentFrame=frameCheck,
            page=self,
            name="Dark Library Theme",
            image="dark_steam_library.png",
            tags=["CSS"])
        mainoption6 = mo6.returnMainOption()
        mainoption6.grid(row=5, column=1, sticky=W)
        ###
        self.dropdown6_value = tk.IntVar()
        self.dropdown6 = ttk.Combobox(frameCheck,
                                 font="TkDefaultFont",
                                 values=["steam-library (Shiina)","Dark Library (Thespikedballofdoom)"],
                                 state="readonly",
                                 textvariable=self.dropdown6_value,
                                 width=30)
        self.dropdown6.current(0)
        self.dropdown6.grid(row=6, column=1, columnspan=2, sticky="w")
        
        
        ###
        label_end = tk.Label(frameCheck, height=0)
        label_end.grid(row=7, column=0, columnspan=2)

        ###
        self.image1 = add_img(frameCheck, resource_path('full_layout.png'))
        self.image1.grid(row=0, column=4, rowspan=8, padx=5, sticky="n")

    ### LOG FRAME
    ###
        frameLog = tk.Frame(self)

        ### Text
        entry1 = ttk.Entry(frameLog)
        self.text1 = tk.Text(entry1, height=12)
        self.text1.configure(font=("Arial",10))
        #self.text1.tag_configure("err", foreground="red")
        ### REDIRECT STDOUT STDERR
        if not DEBUG_STDOUT_STDERR:
            sys.stdout = StdoutRedirector(self.text1)
            sys.stderr = StderrRedirector(self.text1)
        
        self.text1.pack()
        entry1.grid(row=0, column=0)

        ###
        scroll_1 = ttk.Scrollbar(frameLog, command=self.text1.yview)
        scroll_1.grid(row=0, column=1, sticky='ns')
        self.text1['yscrollcommand'] = scroll_1.set
        

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
        button_n.bind("<Button-1>", lambda event:controller.show_frame(PageTwo))
        button_n.grid(row=0, column=1, padx=5)

        
    ### CONFIRM FRAME
    ###
        frameConfirm = confirm_frame(self, controller)


        ### Set GUI from config
        self.loaded_config = set_selected_from_config(self)
        self.text1.config(state='disabled')
        init_cb_check(self.var1, [check2, check3, check5])
        init_cb_check(self.var3, [check4])

    ### Pack frames
        self.frameHead.pack()
        frameCheck.pack()
        frameLog.pack(pady=(10,0))
        frameConfirm.pack(pady=(7, 20), side="bottom")
        frameMode.pack(pady=(2, 0), side="bottom")

    ### Getters
    def getCheckbuttonVal(self, getter):
        return getattr(self, getter)
    def getTextArea(self, getter):
        return getattr(self, getter)

class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

    ### HEAD FRAME
    ###
        self.frameHead = head_frame(self, controller)
        
    ### CHECK FRAME
    ###
        frameCheck = tk.Frame(self)

    ### CSS Frame
    ###
        self.frameCSS = tk.Frame(self)
        self.css_gui = CSSGUICreator(self, controller, backend.load_css_configurables())
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
        button_n.bind("<Button-1>", lambda event:controller.show_frame(PageTwo))
        button_n.grid(row=0, column=1, padx=5)

    ### CONFIRM FRAME
    ###
        frameConfirm = confirm_frame(self, controller)
        
    ### Pack frames
        self.frameHead.pack()
        frameCheck.pack()
        self.frameCSS.pack(fill="both", expand=True, padx=10)
        frameConfirm.pack(pady=(7, 20), side="bottom")
        frameMode.pack(pady=(2, 0), side="bottom")

        #self.frameCSS = create_css_gui(self, controller, backend.load_css_configurables())

class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

    ### HEAD FRAME
    ###
        self.frameHead = head_frame(self, controller)

    ### CHECK FRAME
    ###
        frameCheck = tk.Frame(self)

        label0 = tk.Label(frameCheck,
                          text="Coming Soon")
        label0.grid(row=0, column=0, columnspan=2)
        ###
        self.var1 = tk.IntVar()
        check1 = ttk.Checkbutton(frameCheck,
                                 variable=self.var1,
                                 state='disabled')
        check1.grid(row=1, column=0)
        label1 = tk.Label(frameCheck,
                          text="  - AdvOption1")
        label1.grid(row=1, column=1, sticky="w")
        
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
        self.frameHead.pack()
        frameCheck.pack()
        frameConfirm.pack(pady=(7, 20), side="bottom")
        frameMode.pack(pady=(2, 0), side="bottom")

### FRAME functions
### ================================
def head_frame(self, controller):
    ### HEAD FRAME
    ###
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

def confirm_frame(self, controller):
    frameConfirm = tk.Frame(self)
    ###
    button1 = ttk.Button(frameConfirm,
                       text="Install",
                       width=15                       
    )
    button1.bind("<Button-1>",
                 lambda event:globals()["install_click"](event, self, controller)
                 )
    button1.grid(row=0, column=0, padx=5)
    
    ###
    button2 = ttk.Button(frameConfirm,
                       text="Reload Config",
                       width=15#,
                       ###state='disabled'
    )
    button2.bind("<Button-1>",
                 lambda event:reload_click(event, controller)
                 )
    button2.grid(row=0, column=1, padx=5)
    return frameConfirm
### ================================

### Show Page Functions
def show_PageOne(controller):
    controller.css_config = backend.load_css_configurables()
    controller.show_frame(PageOne)
    #controller.frames[PageOne].frameCSS = create_css_gui(controller.frames[PageOne], controller, backend.load_css_configurables())
    update_css_gui(controller.frames[PageOne], controller, backend.load_css_configurables())

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
### may rewrite, so array of checkboxes instead of separate arguments
### rewritten, but still the two functions
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



### Label + CodeTag
### Kwargs expected
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
        self.label.grid(row=0, column=0, sticky=W)

        for i, tagName in enumerate(kwargs["tags"], start=1):
            leftPadding = (5, 0) if i == 1 else 0
            tag = add_img(self.tagFrame, globals()["resource_path"]('tag_'+tagName+'.png'), width=50)
            tag.grid(row=0, column=i, sticky=W, padx=leftPadding)
            self.tags[self.name]=tag
    def returnMainOption(self):
        return self.tagFrame

    
        
### INSTALL Functions
  
### Map config values to selected checkboxes
CONFIG_MAP = {"SteamLibraryPath" : {"set" : ""},
              "PatcherPath" : {"set" : ""},
              "" : {},
              "InstallCSSTweaks" : {"value" : "var1", "javascript" : False},
              "EnablePlayButtonBox" : {"value" : "var2", "javascript" : False},
              "EnableVerticalNavBar" : {"value" : "var3", "javascript" : True},
              "EnableClassicLayout" : {"value" : "var4", "javascript" : True},
              "LandscapeImages" : {"value" : "var5", "javascript" : True},
              "InstallWithDarkLibrary" : {"value" : "var6", "javascript" : False}
              }

def install_click(event, page, controller):
    #get settings
    settings_to_apply, settings_values = get_settings_from_gui(event, page)
    #applying settings
    apply_settings_from_gui(page, settings_to_apply, settings_values, controller.css_config)
    backend.write_config(settings_values)
    
def get_settings_from_gui(event, page):
    try:
        settings = []
        settings_values = {}
        for key in CONFIG_MAP:
            if "value" in CONFIG_MAP[key]:         
                settings_values[key] = page.getCheckbuttonVal(CONFIG_MAP[key]["value"]).get()
                if page.getCheckbuttonVal(CONFIG_MAP[key]["value"]).get() == 1:
                    settings.append(key)
            elif "set" in CONFIG_MAP[key]:
                settings_values[key] = CONFIG_MAP[key]["set"]    
            else:
                settings_values[""] = ""
        #print("ARRAY ")
        settings_to_apply = backend.validate_settings(settings)
        print(settings_to_apply)
        print(settings_values)
        return settings_to_apply, settings_values
        
    except FileNotFoundError:
        pass
        print("libraryroot.custom.css not found", file=sys.stderr)

def apply_settings_from_gui(page, settings_to_apply, settings_values, root_config):
    print("Applying CSS settings...")
    page.text1.update_idletasks()
    backend.write_css_settings(settings_to_apply, settings_values, root_config)
    page.text1.update_idletasks()

    ### Run js_tweaker if required
    #need_javascript = 0
    #for setting in settings_to_apply:
    #    if CONFIG_MAP[setting]["javascript"]:
    #        need_javascript = 1
    #if need_javascript == 1:
    #    run_js_tweaker(page.text1)

    change_javascript = 0
    for setting in settings_values:
        #print("javascript" in CONFIG_MAP[setting])
        if "javascript" in CONFIG_MAP[setting]:
            if CONFIG_MAP[setting]["javascript"] \
            and int(page.loaded_config[setting]) != page.getCheckbuttonVal(CONFIG_MAP[setting]["value"]).get():
                print(int(page.loaded_config[setting]))
                print(page.getCheckbuttonVal(CONFIG_MAP[setting]["value"]).get())
                change_javascript = 1
        
    if change_javascript == 1:
        run_js_tweaker(page.text1)
    
    print("Settings applied.")
    
def run_js_tweaker(text_area):
    ###with open('js_tweaker.py') as source_file:
    try:
        print("==================")
        print("Running js_tweaker")
        text_area.update_idletasks()

        ###
        js_tweaker.beautify_js()
        text_area.update_idletasks()
        js_tweaker.setup_library()
        text_area.update_idletasks()
        js_tweaker.parse_fixes_file("fixes.txt")
        text_area.update_idletasks()
        js_tweaker.write_modif_file()
        text_area.update_idletasks()
        js_tweaker.re_minify_file()
        text_area.update_idletasks()
        print("\nSteam Library JS Tweaks applied successfully.")
              
    except Exception as e:
        print(e, file=sys.stderr)



### RELOAD Functions
### ================================
def reload_click(event, controller):
    #.frames[StartPage].text1
    controller.css_config = backend.load_css_configurables()
    #print(controller.css_config["What's New"])



### Image Functions

def open_img(filename, width=350):
    x = filename
    img = Image.open(x)
    new_width = width
    new_height = int(new_width * img.height / img.width)
    img = img.resize((new_width, new_height), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    return img

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
class Detail_tooltip(OnHoverTooltipBase):
    def __init__(self, anchor_widget, text, hover_delay=1000):
        super(Detail_tooltip, self).__init__(anchor_widget, hover_delay=hover_delay)
        self.text = text
        
    def showcontents(self):
        message = Message(self.tipwindow, text=self.text, justify=LEFT,
                      background="#ffffe0", width=590, relief=SOLID, borderwidth=1)
        message.pack()
        
### Initialisation
def set_selected_from_config(page):
    ### grab stdout, stderr from function in backend
    f = io.StringIO()
    loaded_config = backend.load_config()
    #with contextlib.redirect_stdout(f):   
    for key in loaded_config:
        if key in CONFIG_MAP :
            if loaded_config[key] == '0' :
                page.getCheckbuttonVal(CONFIG_MAP[key]["value"]).set(0)
            if loaded_config[key] == '1' :
                page.getCheckbuttonVal(CONFIG_MAP[key]["value"]).set(1)
    return loaded_config



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
        y = PresetFrame(self.frameCSS, controller, config)
        self.framePreset = y.returnPresetFrame()

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
            print(traceback.print_exc(), file=sys.stderr)
            print("CSS config in libraryroot.custom.css not configured correctly.\n", file=sys.stderr)
            print("Either the format of configurable variables is incorrect or this feature is not fully implemented yet.\n", file=sys.stderr)

    def returnCSSConfigRow(self):
        return self.frameCSSRow



###
### END ConfigurablesFrame
          
class PresetFrame(tk.Frame):
    def __init__(self, parent, controller, config):
        self.parent = parent
        self.framePreset = tk.Frame(self.parent)
        self.controller = controller
        self.config = config
            
        label_preset_head = tk.Label(self.framePreset, text="Quick CSS Settings")
        label_preset_head.grid(row=0, column=0)
        '''
        button1 = ttk.Button(self.framePreset,
                        text="What's New",
                        width=12
        )
        
        button1.bind("<Button-1>",
                    lambda event:globals()["preset_click"](event, controller,
                    {
                        "--WhatsNew" : "block",
                        "--WhatsNewOrder" : "2"
                    })
                    )
        
        button1.grid(row=1, column=0, padx=(5,0))
        '''

        label1 = tk.Label(self.framePreset, text="What's New")
        label1.grid(row=1, column=0, padx=(5,0))

        self.radios_config = {"Bottom of page" : {"value" : "1", "config" : 
                            {"--WhatsNew" : "block",
                            "--WhatsNewOrder" : "2"}},
                  "Hide entirely" : {"value" : "2", "config" :
                            {"--WhatsNew" : "none",
                            "--WhatsNewOrder" : "0"}},
                "Higsegs" : {"value" : "3", "config" :
                            {"--WhatsNew" : "black",
                            "--WhatsNewOrder" : "17"}}
                  }
        self.radiovar = tk.StringVar()
        self.radiovar.set("1")
        self.radios = {}

        radio1_text = "Bottom of page"
        radio1 = ttk.Radiobutton(self.framePreset,
                            text = radio1_text, 
                            variable = self.radiovar,
                            value = "1",
                            command = lambda: self.preset_click(controller, radio1_text)
                            )
        radio1.grid(row=3, column=0, padx=(5,0), sticky='w')
        
        
    ### PRESET Click funtion
    def preset_click(self, controller, radioText):
        #self.radiovar.set(self.radios_config[radioText]["value"])
        print("~~~pcccc~~~~~~")
        print(radioText)
        #print(self.radios_config[radioText]["config"])
        #print("APPLY")
        globals()["apply_css_config_values"](controller, self.radios_config[radioText]["config"])
        #print("~~~~~~~~~~~")
        #print(controller.css_config)
        
    def returnPresetFrame(self):
        return self.framePreset

### Preset
### ~~~~~~~~~~
### change container.css_config
### Recursion
def apply_css_config_values(controller, propValues):
    print("~~~pv~~~~~~~~~~")
    print(propValues)
    returns = []
    for key, value in propValues.items():
        controller.config_dict = replace_item(key, value, controller.css_config)
    #print(controller.css_config)
    print("~~~g~")
    #print(controller.css_config)

    
            
### Recursion 
        #key, replace_value obj

'''
def replace_item(obj, key, replace_value):
    for k, v in obj.items():
        if isinstance(v, dict):
            obj[k] = replace_item(v, key, replace_value)
    if key in obj:
        obj[key] = replace_value
    return obj
'''
def replace_item(key, value, config_dict):
    for k, v in config_dict.items():
        if isinstance(v, dict):
            config_dict[k] = replace_item(key, value, v)
    if key in config_dict:
        print("wAZOO")
        print(str(key) + "~~" + str(value))
        print(config_dict[key]["current"])
        config_dict[key]["current"] = value
        #print("CHANGED")
        print(config_dict[key]["current"])
    return config_dict
###
### ~~~~~~~~~~

def update_css_gui(page, controller, config):
    #print(page.frameCSS)
    #print(dir(page.frameCSS))
    test_css_gui_reach(page, controller, config)

    #for entrybox in page.css_gui.entryboxes:
        #config.get(sectionkey, {}).get(propkey)

def test_css_gui_reach(page, controller, config):
    print("TODO")
    #print(page.css_gui.labels[0]["text"])
    #print(page.css_gui.entryboxes["--WhatsNew"].get())
    #print(page.css_gui.entryboxes["--WhatsNew"].set("lamb"))

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
#create_user_config_from_gui():        


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def main():
    app = OldGloryApp()
    app.mainloop()

if __name__ == "__main__":
    main()
