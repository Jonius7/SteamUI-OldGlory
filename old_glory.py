import tkinter as tk
import tkinter.font as TkFont
from tkinter import ttk
from PIL import ImageTk, Image
import cssutils
import backend


class OldGloryApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        windowW = 700
        windowH = 400
        self.geometry((str(windowW)+'x'+str(windowH)+'+950+400'))
        self.minsize(width=windowW, height=windowH)
        self.maxsize(width=windowW, height=windowH)
        container.pack(side="top", fill="both", expand = True)
        
        self.iconbitmap('steam_oldglory.ico')
        self.wm_title("SteamUI-OldGlory Configurer")
        ###frameTitle = tk.Frame()

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

        for F in (StartPage, PageOne):
            frame = F(container, self)
            frame.grid(row=0, column=0, sticky="nsew")
            self.frames[F] = frame
        self.show_frame(StartPage)

    def show_frame(self, cont):
        self.frames[cont].tkraise()

    def load_from_config():
        print("yahoo")

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        frameHead = head_frame(self, controller)


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
        image1.grid(row=0, column=2, rowspan=5, padx=5, sticky="n")
        
        ###
        self.var3 = tk.IntVar()
        check3 = ttk.Checkbutton(frameCheck,
                                 variable=self.var3,
                                 state='disabled')
        check3.grid(row=2, column=0)
        label3 = tk.Label(frameCheck,
                          text="  - Vertical Nav Bar")
        label3.grid(row=2, column=1, sticky="w")

        ###
        self.var4 = tk.IntVar()
        check4 = ttk.Checkbutton(frameCheck,
                                 variable=self.var4)
        check4.grid(row=3, column=0)
        label4 = tk.Label(frameCheck,
                          text="Install with Dark Library (steam-library)")
        label4.bind("<Button-1>", lambda event:change_image(image1, 'dark_steam_library.png'))
        label4.grid(row=3, column=1, sticky="w")

        ###
        label_end = tk.Label(frameCheck, height=5)
        label_end.grid(row=4, column=0, columnspan=2)
        

        ### MODE Frame
        ###
        frameMode = tk.Frame(self)
        self.var_m = tk.IntVar()
        button_m = ttk.Button(frameMode,
                           text="Advanced Options",
                           width=20
        )
        ###button_m.bind("<Button-1>", lambda event:controller.show_frame(PageOne))
        button_m.config(command=lambda: controller.show_frame(PageOne))
        button_m.grid(row=0, column=0, padx=5)

        
        ### CONFIRM FRAME
        ###
        ###frameConfirm = confirm_frame(self.var1, frameHead.labeltext_b)

        ###
        frameHead.pack()
        frameCheck.pack()
        frameMode.pack(pady=8)
        ###frameConfirm.pack()

class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        frameCheck = tk.Frame(self)
        self.var3 = tk.IntVar()
        check3 = ttk.Checkbutton(frameCheck,
                                 variable=self.var3,
                                 state='disabled')
        check3.grid(row=2, column=0)
        label3 = tk.Label(frameCheck,
                          text="  - Vertical Nav Bar")
        label3.grid(row=2, column=1, sticky="w")
        self.var3 = tk.IntVar()
        check3 = ttk.Checkbutton(frameCheck,
                                 variable=self.var3,
                                 state='disabled')
        check3.grid(row=2, column=0)
        label3 = tk.Label(frameCheck,
                          text="  - Vertical Nav Bar")
        label3.grid(row=2, column=1, sticky="w")
        self.var3 = tk.IntVar()
        check3 = ttk.Checkbutton(frameCheck,
                                 variable=self.var3,
                                 state='disabled')
        check3.grid(row=2, column=0)
        label3 = tk.Label(frameCheck,
                          text="  - Vertical Nav Bar")
        label3.grid(row=2, column=1, sticky="w")
        
        ### MODE Frame
        ###
        frameMode = tk.Frame(self)
        self.var_m = tk.IntVar()
        button_m = ttk.Button(frameMode,
                           text="Options",
                           width=20
        )
        button_m.bind("<Button-1>", lambda event:controller.show_frame(StartPage))
        button_m.grid(row=0, column=0, padx=5)
        
        ###frameConfirm = confirm_frame(tk.IntVar(), tk.StringVar())
        frameCheck.pack()
        frameMode.pack(pady=8)
        ###frameConfirm.pack()

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
    labeltext_b = tk.StringVar()
    labeltext_b.set("A set of CSS and JS tweaks for the Steam Library")
        
    label_b = tk.Label(frameHead, textvariable=labeltext_b)
    label_b.grid(row=1, column=0)
    return frameHead

def confirm_frame(checked, labeltext):
    frameConfirm = tk.Frame()
    ###
    button1 = ttk.Button(frameConfirm,
                       text="Install",
                       width=15                       
    )
    button1.bind("<Button-1>", lambda event:install_click(event, checked, labeltext))
    button1.grid(row=0, column=0, padx=5)

    button2 = ttk.Button(frameConfirm,
                       text="Load from Config",
                       width=15,
                       state='disabled'
    )
    button2.bind()
    button2.grid(row=0, column=1)
    return frameConfirm


def css_cb_check(event, var1, check2, check3):
    if var1.get() == 0:
        check2.config(state='enabled')
        check3.config(state='enabled')
    else:
        check2.config(state='disabled')
        check3.config(state='disabled')


def install_click(event, var1, labeltext):
    if var1.get() == 1:
        labeltext.set("var enabled " + str(var1.get()))
    else:
        labeltext.set("var disabled " + str(var1.get()))

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

### Initialisation
   
def main():
    app = OldGloryApp()
    app.mainloop()

if __name__ == "__main__":
    main()
