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

OS_TYPE = platform.system()

class OldGloryApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        windowW = 700
        windowH = 600
        self.geometry((str(windowW)+'x'+str(windowH)+'+650+300'))
        self.minsize(width=windowW, height=windowH)
        self.maxsize(width=windowW, height=windowH)
        container.pack(side="top", fill="both", expand = True)
        
        if OS_TYPE == "Windows":
            self.iconbitmap(resource_path('steam_oldglory.ico'))
        self.wm_title("SteamUI-OldGlory Configurer")

        

        ###
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
        
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

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
        frameCheck.grid_columnconfigure(2, weight=1)
        
        ######
        self.var1 = tk.IntVar()
        check1 = ttk.Checkbutton(frameCheck,
                                 variable=self.var1
                                 )
                                 
        check1.bind("<Button-1>", lambda event:css_cb_check(event, self.var1, check2, check3))
        check1.grid(row=0, column=0)
        ###
        tagFrame1 = tk.Frame(frameCheck)
        label1 = tk.Label(tagFrame1,
                          text="Install CSS Tweaks",
                          cursor="hand2")
        label1.bind("<Button-1>", lambda event:change_image(image1, resource_path('buttons_before_after.png')))
        #label1.grid(row=0, column=1, columnspan=1, sticky="w")
        label1.grid(row=0, column=0, sticky=W)
        ###
        tag1a = add_img(tagFrame1, resource_path('tag_CSS.png'), width=50)
        tag1a.grid(row=0, column=1, sticky=W, padx=(5,0))
        tagFrame1.grid(row=0, column=1, sticky=W)


        ######
        self.var2 = tk.IntVar()
        check2 = ttk.Checkbutton(frameCheck,
                                 variable=self.var2,
                                 state='disabled')
        check2.grid(row=1, column=0)
        ###
        tagFrame2 = tk.Frame(frameCheck)
        label2 = tk.Label(tagFrame2,
                          text="  \u2937 Box Play Button",
                          cursor="hand2")
        label2.bind("<Button-1>", lambda event:change_image(image1, resource_path('play_button_box.png')))
        #label2.grid(row=1, column=1, columnspan=1, sticky="w")
        label2.grid(row=0, column=0, sticky=W)
        ###
        tag2a = add_img(tagFrame2, resource_path('tag_CSS.png'), width=50)
        tag2a.grid(row=0, column=1, sticky=W, padx=(5,0))
        tagFrame2.grid(row=1, column=1, sticky=W)

        
        ######
        self.var3 = tk.IntVar()
        check3 = ttk.Checkbutton(frameCheck,
                                 variable=self.var3,
                                 state='disabled')
        check3.bind("<Button-1>", lambda event:css_cb_check(event, self.var3, check4, check4))
        check3.grid(row=2, column=0)
        ###
        tagFrame3 = tk.Frame(frameCheck)
        label3 = tk.Label(tagFrame3,
                          text="  \u2937 Vertical Nav Bar",
                          cursor="hand2")
        label3.bind("<Button-1>", lambda event:change_image(image1, resource_path('vertical_nav_bar.png')))
        label3.grid(row=0, column=0, columnspan=1, sticky="w")
        ###
        tag3a = add_img(tagFrame3, resource_path('tag_CSS.png'), width=50)
        tag3a.grid(row=0, column=1, sticky=W, padx=(5,0))
        tag3b = add_img(tagFrame3, resource_path('tag_JS.png'), width=50)
        tag3b.grid(row=0, column=2, sticky=W)
        tagFrame3.grid(row=2, column=1, sticky=W)
        
        
        ######
        self.var4 = tk.IntVar()
        check4 = ttk.Checkbutton(frameCheck,
                                 variable=self.var4,
                                 state='disabled'
                                 )
        check4.grid(row=3, column=0)
        ###
        tagFrame4 = tk.Frame(frameCheck)
        label4 = tk.Label(tagFrame4,
                          text="    \u2937 Classic Layout",
                          cursor="hand2")
        label4.bind("<Button-1>", lambda event:change_image(image1, resource_path('classic_layout.png')))
        label4.grid(row=0, column=0, columnspan=1, sticky="w")
        ###
        tag4a = add_img(tagFrame4, resource_path('tag_CSS.png'), width=50)
        tag4a.grid(row=0, column=1, sticky=W, padx=(5,0))
        tag4b = add_img(tagFrame4, resource_path('tag_JS.png'), width=50)
        tag4b.grid(row=0, column=2, sticky=W)
        tagFrame4.grid(row=3, column=1, sticky=W)

        
        ######
        self.var5 = tk.IntVar()
        check5 = ttk.Checkbutton(frameCheck,
                                 variable=self.var5)
        check5.grid(row=4, column=0)
        ###
        tagFrame5 = tk.Frame(frameCheck)
        label5 = tk.Label(tagFrame5,
                          text="Dark Library Theme",
                          cursor="hand2")
        label5.bind("<Button-1>", lambda event:change_image(image1, resource_path('dark_steam_library.png')))
        label5.grid(row=0, column=0, columnspan=1, sticky="w")
        ###
        tag5a = add_img(tagFrame5, resource_path('tag_CSS.png'), width=50)
        tag5a.grid(row=0, column=1, sticky=W, padx=(5,0))
        tagFrame5.grid(row=4, column=1, sticky=W)
        ###
        self.dropdown5_value = tk.IntVar()
        self.dropdown5 = ttk.Combobox(frameCheck,
                                 font="TkDefaultFont",
                                 values=["steam-library (Shiina)","Dark Library (Thespikedballofdoom)"],
                                 state="readonly",
                                 textvariable=self.dropdown5_value,
                                 width=30)
        self.dropdown5.current(0)
        self.dropdown5.grid(row=5, column=1, columnspan=2, sticky="w")
        
        
        ###
        label_end = tk.Label(frameCheck, height=2)
        label_end.grid(row=6, column=0, columnspan=2)

        ###
        image1 = add_img(frameCheck, resource_path('buttons_before_after.png'))
        image1.grid(row=0, column=4, rowspan=7, padx=5, sticky="n")

    ### LOG FRAME
    ###
        frameLog = tk.Frame(self)

        ### Text
        entry1 = ttk.Entry(frameLog)
        self.text1 = tk.Text(entry1, height=12)
        self.text1.configure(font=("Arial",10))
        self.text1.tag_configure("err", foreground="red")

        ### REDIRECT STDOUT STDERR
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
        button_m.bind("<Button-1>", lambda event:controller.show_frame(PageOne))
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
        frameConfirm = confirm_frame(self)


        ### Set GUI from config
        set_selected_from_config(self)
        self.text1.config(state='disabled')
        init_cb_check(self.var1, check2, check3)
        init_cb_check(self.var3, check4, check4)

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
        self.frameCSS = css_config_to_gui(self, controller, backend.CSS_CONFIG)
        
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
        frameConfirm = confirm_frame(self)
        
    ### Pack frames
        self.frameHead.pack()
        frameCheck.pack()
        #canvasCSS.pack(fill="both", expand=True)
        self.frameCSS.pack(fill="both", expand=True, padx=10)
        frameConfirm.pack(pady=(7, 20), side="bottom")
        frameMode.pack(pady=(2, 0), side="bottom")

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
        button_n.bind("<Button-1>", lambda event:controller.show_frame(PageOne))
        button_n.grid(row=0, column=1, padx=5)

    ### CONFIRM FRAME
    ###
        frameConfirm = confirm_frame(self)

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

def confirm_frame(self):
    frameConfirm = tk.Frame(self)
    ###
    button1 = ttk.Button(frameConfirm,
                       text="Install",
                       width=15                       
    )
    button1.bind("<Button-1>",
                 lambda event:globals()["get_settings_from_gui"](event, self)
                 )
    button1.grid(row=0, column=0, padx=5)
    
    ###
    button2 = ttk.Button(frameConfirm,
                       text="Reload Config",
                       width=15#,
                       ###state='disabled'
    )
    button2.bind("<Button-1>",
                 lambda event:reload_click(event, self.text1)
                 )
    button2.grid(row=0, column=1, padx=5)
    return frameConfirm
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
        self.text_area.config(foreground="red")
        self.text_area.insert(tk.END, text)
        self.text_area.yview_pickplace("end")
        self.text_area.config(state='disabled')        
    def flush(self):
        pass

### ================================

### Checkbox Validation - Disable
### ================================
### may rewrite, so array of checkboxes instead of separate arguments
def css_cb_check(event, var1, check2, check3):
    if var1.get() == 0:
        check2.config(state='enabled')
        check3.config(state='enabled')
    else:
        check2.config(state='disabled')
        check3.config(state='disabled')
        
def init_cb_check(var1, check2, check3):
    if var1.get() == 1:
        check2.config(state='enabled')
        check3.config(state='enabled')
    else:
        check2.config(state='disabled')
        check3.config(state='disabled')
### ================================



### GUI CODE TAGS (CSS, JS, Skin)
#def create_code_tag(langs): 
    
        
### INSTALL Functions
        
   


### RELOAD Functions
### ================================
def reload_click(event, text_area):
    backend.load_css_options()
    print(text_area)
    run_js_tweaker(text_area)
    
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

### Map config values to selected checkboxes
CONFIG_MAP = {"InstallCSSTweaks" : "var1",
              "EnablePlayButtonBox" : "var2",
              "EnableVerticalNavBar" : "var3",
              "EnableClassicLayout" : "var4",
              "InstallWithDarkLibrary" : "var5"}

        
def get_settings_from_gui(event, page):
    try:
        settings = []
        for key in CONFIG_MAP:
            #print(page.getCheckbuttonVal(CONFIG_MAP[key]).get())
            if page.getCheckbuttonVal(CONFIG_MAP[key]).get() == 1:
                settings.append(key)
                #print(key)
        #print("ARRAY ")
        settings_to_apply = backend.validate_settings(settings)
        print(settings_to_apply)
        #applying settings
        apply_settings_from_gui(page, settings_to_apply)
    except FileNotFoundError:
        pass
        #print("libraryroot.custom.css not found", file=sys.stderr)

def apply_settings_from_gui(page, settings_to_apply):
    print("Applying settings...")
    page.text1.update_idletasks()
    backend.apply_settings(settings_to_apply)
    print("Settings applied.")
        
### Initialisation
def set_selected_from_config(page):
    
    ### grab stdout, stderr from function in backend
    f = io.StringIO()
    #with contextlib.redirect_stdout(f):
    loaded_config = backend.load_config()
        
        
    for key in loaded_config:
        if key in CONFIG_MAP :
            if loaded_config[key] == '0' :
                page.getCheckbuttonVal(CONFIG_MAP[key]).set(0)
            if loaded_config[key] == '1' :
                page.getCheckbuttonVal(CONFIG_MAP[key]).set(1)
        else :
            None

### CSS Config to GUI
def css_config_to_gui(self, controller, config):
    ###Outer frame and canvas
    cssOptionsFrame = tk.Frame(self)
    frameCSSOuter = css_frame(cssOptionsFrame, controller, config)
    framePreset = css_preset_frame(cssOptionsFrame, controller, config)

    #Configure grid expand
    cssOptionsFrame.columnconfigure(0, weight=2)
    cssOptionsFrame.rowconfigure(0, weight=1)
    cssOptionsFrame.columnconfigure(1, weight=1)
    
    framePreset.grid(row=0, column=0, sticky="nsew")
    frameCSSOuter.grid(row=0, column=1, sticky="nsew")
    #frameCSSOuter.pack(fill="both", expand=True, padx=10)
    
    return cssOptionsFrame

def css_frame(parent, controller, config):
    frameCSSOuter = tk.Frame(parent)
    
    canvasCSS = tk.Canvas(frameCSSOuter, highlightthickness=0, yscrollincrement=10) #remove highlight black border wtf
    canvasCSS.pack(side="left")
    #canvasCSS.grid(row=0, column=0, padx=10, sticky="nsew")
    

    ### Scrollbar
    scroll_1 = ttk.Scrollbar(frameCSSOuter, command=canvasCSS.yview)
    scroll_1.pack(side="right", fill="y")
    #scroll_1.grid(row=0, column=1, sticky="nsew")
    canvasCSS.configure(yscrollcommand=scroll_1.set)
    canvasCSS.bind('<Configure>', lambda e: canvasCSS.configure(scrollregion = canvasCSS.bbox('all')))
    
    ### Inner frame
    frameCSS = tk.Frame(canvasCSS)
    canvasCSS.create_window((0,0), window=frameCSS, anchor="nw")
    canvasCSS.pack(fill=BOTH, expand=YES)
    
    ### Section title font
    sectionfont = controller.default_font.copy()
    sectionfont.configure(underline=1)
    
    ### Populate config
    labels = []
    row = -1
    
    for i, section in enumerate(config):
        row += 1
        label = tk.Label(frameCSS,
                          text=section,
                         font=sectionfont,
                         fg='blue')
        label.grid(row=row, column=0)
        labels.append(label)
        
        labelgroup = []
        for j, prop in enumerate(config[section]):
            #print(config[section][prop]['options'])
            propDict = config[section][prop]
            frameCSSSection = create_css_config_row(prop, propDict, frameCSS)
            row += 1

            
            frameCSSSection.grid(row=row, column=0, padx=(15, 0))
    return frameCSSOuter

def css_preset_frame(parent, controller, config):
    framePreset = tk.Frame(parent)#,bd=2,relief=tk.SOLID)

    preset_head = tk.StringVar()
    preset_head.set("Quick CSS Settings")
        
    label_preset_head = tk.Label(framePreset, textvariable=preset_head)
    label_preset_head.grid(row=0, column=0)
    
    
    button1 = ttk.Button(framePreset,
                       text="What's New",
                         state="disabled",
                       width=12                       
    )
    #button1.bind("<Button-1>",
                 #lambda event:globals()["get_settings_from_gui"](event, self)
                 #)
    button1.grid(row=1, column=0, padx=(5,0))
    return framePreset
    

###Structure of CSS config as follows
###config       > section       > prop              > attr
###CSS_CONFIG   > "What's New"  > "--WhatsNewOrder" > "desc" 
def create_css_config_row(propName, propDict, parentFrame):
    frameCSSRow = tk.Frame(parentFrame)
    try:
        
        label = tk.Label(frameCSSRow,
                          text=propName,anchor='w',width=25)
        tip = Detail_tooltip(label, formatted_hover_text(propDict['default'], propDict['desc']), hover_delay=200)
        label.grid(row=0, column=0)
        
        combobox = ttk.Combobox(frameCSSRow,
                                font="TkDefaultFont",
                                 values=get_prop_options_as_array(propDict),
                                width=12)
        combobox.set(propDict['current'])
        combobox.grid(row=0, column=1, pady=1)
        
        '''
        var2 = tk.IntVar()
        check2 = ttk.Checkbutton(frameCSSRow,
                                 variable=var2)
        check2.grid(row=0, column=1)
            #print("WAXOO " + propDict['default'])
        '''
    except Exception as e:
        print(e, file=sys.stderr)
        print("CSS config in libraryroot.custom.css not configured correctly.\n", file=sys.stderr)
        print("Either the format of configurable variables is incorrect or this feature is not fully implemented yet.\n", file=sys.stderr)

    return frameCSSRow

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
