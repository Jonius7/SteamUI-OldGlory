import tkinter as tk
import tkinter.font as TkFont
from tkinter import ttk
from PIL import ImageTk, Image
import sys
import contextlib, io
import backend
import js_tweaker
import os


class OldGloryApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        windowW = 700
        windowH = 500
        self.geometry((str(windowW)+'x'+str(windowH)+'+650+400'))
        self.minsize(width=windowW, height=windowH)
        self.maxsize(width=windowW, height=windowH)
        container.pack(side="top", fill="both", expand = True)
        
        #self.iconbitmap('steam_oldglory.ico')
        self.wm_title("SteamUI-OldGlory Configurer")

        ###
        

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
        
        ###
        self.var1 = tk.IntVar()
        check1 = ttk.Checkbutton(frameCheck,
                                 variable=self.var1
                                 )
                                 
        check1.bind("<Button-1>", lambda event:css_cb_check(event, self.var1, check2, check3))
        check1.grid(row=0, column=0)
        label1 = tk.Label(frameCheck,
                          text="Install CSS Tweaks (SteamUI-OldGlory)")
        label1.bind("<Button-1>", lambda event:change_image(image1, 'buttons_before_after.png'))
        label1.grid(row=0, column=1, sticky="w")

        ###
        self.var2 = tk.IntVar()
        check2 = ttk.Checkbutton(frameCheck,
                                 variable=self.var2,
                                 state='disabled')
        check2.grid(row=1, column=0)
        label2 = tk.Label(frameCheck,
                          text="  - Box Play Button")
        label2.bind("<Button-1>", lambda event:change_image(image1, 'play_button_box.png'))
        label2.grid(row=1, column=1, sticky="w")
        
        ###
        image1 = add_img(frameCheck, 'buttons_before_after.png')
        image1.grid(row=0, column=2, rowspan=6, padx=5, sticky="n")
        
        ###
        self.var3 = tk.IntVar()
        check3 = ttk.Checkbutton(frameCheck,
                                 variable=self.var3,
                                 state='disabled')
        check3.bind("<Button-1>", lambda event:css_cb_check(event, self.var3, check4, check4))
        check3.grid(row=2, column=0)
        label3 = tk.Label(frameCheck,
                          text="  - Vertical Nav Bar")
        label3.bind("<Button-1>", lambda event:change_image(image1, 'vertical_nav_bar.png'))
        label3.grid(row=2, column=1, sticky="w")
        
        ###
        self.var4 = tk.IntVar()
        check4 = ttk.Checkbutton(frameCheck,
                                 variable=self.var4,
                                 state='disabled'
                                 )
        check4.grid(row=3, column=0)
        label4 = tk.Label(frameCheck,
                          text="    - Classic Layout")
        label4.bind("<Button-1>", lambda event:change_image(image1, 'classic_layout.png'))
        label4.grid(row=3, column=1, sticky="w")
        
        ###
        self.var5 = tk.IntVar()
        check5 = ttk.Checkbutton(frameCheck,
                                 variable=self.var5)
        check5.grid(row=4, column=0)
        label5 = tk.Label(frameCheck,
                          text="Install with Dark Library (steam-library)")
        label5.bind("<Button-1>", lambda event:change_image(image1, 'dark_steam_library.png'))
        label5.grid(row=4, column=1, sticky="w")

        ###
        label_end = tk.Label(frameCheck, height=3)
        label_end.grid(row=5, column=0, columnspan=2)


        ### LOG FRAME
        ###
        frameLog = tk.Frame(self)

        ### Text
        entry1 = ttk.Entry(frameLog)
        text1 = tk.Text(entry1, height=5)
        ###text1.insert(tk.END, "Start\r\n")
        text1.tag_configure("err", foreground="red")

        ### REDIRECT STDOUT STDERR
        #sys.stdout = StdoutRedirector(text1)
        #sys.stderr = StderrRedirector(text1)
        
        text1.pack()
        entry1.grid(row=0, column=0)
        
        ###
        scroll_1 = ttk.Scrollbar(frameLog, command=text1.yview)
        scroll_1.grid(row=0, column=1, sticky='nsew')
        text1['yscrollcommand'] = scroll_1.set
        

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
        text1.config(state='disabled')
        init_cb_check(self.var1, check2, check3)
        init_cb_check(self.var3, check4, check4)

        ###
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

        ###
        self.var2 = tk.IntVar()
        check2 = ttk.Checkbutton(frameCheck,
                                 variable=self.var2,
                                 state='disabled')
        check2.grid(row=2, column=0)
        label2 = tk.Label(frameCheck,
                          text="  - AdvOption2")
        label2.grid(row=2, column=1, sticky="w")

        ###
        self.var3 = tk.IntVar()
        check3 = ttk.Checkbutton(frameCheck,
                                 variable=self.var3,
                                 state='disabled')
        check3.grid(row=3, column=0)
        label3 = tk.Label(frameCheck,
                          text="  - AdvOption3")
        label3.grid(row=3, column=1, sticky="w")
        
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
                 lambda event:get_settings_from_gui(event, self)
                 )
    button1.grid(row=0, column=0, padx=5)
    
    ###
    button2 = ttk.Button(frameConfirm,
                       text="Reload Config",
                       width=15#,
                       ###state='disabled'
    )
    button2.bind("<Button-1>",
                 lambda event:reload_click(event)
                 )
    button2.grid(row=0, column=1, padx=5)
    return frameConfirm


### Redirect StdOut

class IORedirector(object):
    def __init__(self, text_area):
        self.text_area = text_area

class StdoutRedirector(IORedirector):
    def write(self, text):
        self.text_area.config(foreground="black")
        self.text_area.insert(tk.END, text)
    def flush(self):
        pass

class StderrRedirector(IORedirector):
    def write(self, text):
        self.text_area.config(foreground="red")
        self.text_area.insert(tk.END, text)
    def flush(self):
        pass


### Checkbox Validation - Disable
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

### INSTALL Functions
        
   


### RELOAD Functions
def reload_click(event):
    backend.load_css_options()
    run_js_tweaker()
    
def run_js_tweaker():
    ###with open('js_tweaker.py') as source_file:
    os.system('python js_tweaker.py')
    print("running, but not")

### Image Functions

def open_img(filename):
    x = filename
    img = Image.open(x)
    new_width = 350
    new_height = int(new_width * img.height / img.width)
    img = img.resize((new_width, new_height), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    return img

def add_img(frame, filename):
    img = open_img(filename)
    panel = tk.Label(frame, image=img)
    panel.image = img
    return panel

def change_image(label, filename):
    img = open_img(filename)
    label.configure(image=img)
    label.image = img


### Map config values to selected checkboxes
CONFIG_MAP = {"InstallCSSTweaks" : "var1",
              "EnablePlayButtonBox" : "var2",
              "EnableVerticalNavBar" : "var3",
              "EnableClassicLayout" : "var4",
              "InstallWithDarkLibrary" : "var5"}

        
def get_settings_from_gui(event, page):
    settings = []
    for key in CONFIG_MAP:
        print(page.getCheckbuttonVal(CONFIG_MAP[key]).get())
        if page.getCheckbuttonVal(CONFIG_MAP[key]).get() == 1:
            settings.append(key)
            #print(key)
    #print("ARRAY ")
    #print(settings)


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

def main():
    app = OldGloryApp()
    app.mainloop()

if __name__ == "__main__":
    main()
