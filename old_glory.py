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
        windowW = 600
        windowH = 400
        self.geometry((str(windowW)+'x'+str(windowH)+'+950+400'))
        self.minsize(width=windowW, height=windowH)
        self.maxsize(width=windowW, height=windowH)

        self.iconbitmap('steam_oldglory.ico')
        self.wm_title("SteamUI-OldGlory Configurer")
        frameTitle = tk.Frame()

        ###
        self.default_font = TkFont.nametofont("TkDefaultFont")
        self.default_font.configure(size=13)
        
        ###container.grid(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PageOne):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")
            ###frame.grid(row=110, column=110, sticky="nsew")
        
        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        ### HEAD FRAME
        ###
        frameHead = tk.Frame()
        
        ###
        labeltext1 = tk.StringVar()
        labeltext1.set("SteamUI-OldGlory")
        label1 = tk.Label(frameHead, textvariable=labeltext1, font=(controller.default_font, 20))
        ###label1.pack(padx=20)
        label1.grid(row=0, column=0)

        ###
        labeltext2 = tk.StringVar()
        labeltext2.set("A set of CSS and JS tweaks for the Steam Library")
        label2 = tk.Label(frameHead, textvariable=labeltext2)
        ###label2.pack(padx=20, pady=10)
        label2.grid(row=1, column=0)


        ### CHECK FRAME
        ###
        frameCheck = tk.Frame()
        
        ###
        self.var1 = tk.IntVar()
        check1 = ttk.Checkbutton(frameCheck,
                                 text="Install CSS Tweaks (SteamUI-OldGlory)",
                                 variable=self.var1,
                                 )
                                 
        check1.bind("<Button-1>", lambda event:css_cb_check(event, self.var1, check2, check3))
        check1.grid(row=0, column=0)

        ###
        self.var2 = tk.IntVar()
        check2 = ttk.Checkbutton(frameCheck,
                                 text="- Box Play Button",
                                 variable=self.var2,
                                 state='disabled')
        check2.grid(row=1, column=0)
        
        ###
        image1 = open_img(frameCheck, 'buttons_before_after.png')
        image1.grid(row=0, column=8, rowspan=3)
        
        ###
        self.var3 = tk.IntVar()
        check3 = ttk.Checkbutton(frameCheck,
                                 text="- Vertical Nav Bar",
                                 variable=self.var3,
                                 state='disabled')
        check3.grid(row=2, column=0)

        ###
        self.var4 = tk.IntVar()
        check4 = ttk.Checkbutton(frameCheck, text="Install with Dark Library (steam-library)", variable=self.var4)
        check4.grid(row=3,column=0)
        
        ### CONFIRM FRAME
        ###
        frameConfirm = tk.Frame()
        ###
        button1 = ttk.Button(frameConfirm,
                           text="Install",
                           width=20,                       
        )
        button1.bind("<Button-1>", lambda event:handle_click(event, self.var1, labeltext2))
        button1.grid(column=0)
        
        frameHead.pack()
        frameCheck.pack()
        frameConfirm.pack()

class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

def css_cb_check(event, var1, check2, check3):
    if var1.get() == 0:
        check2.config(state='enabled')
        check3.config(state='enabled')
    else:
        check2.config(state='disabled')
        check3.config(state='disabled')


def handle_click(event, var1, labeltext):
    if var1.get() == 1:
        labeltext.set("var enabled " + str(var1.get()))
    else:
        labeltext.set("var disabled " + str(var1.get()))

def open_img(frame, filename):
    x = filename
    img = Image.open(x)
    new_width = 250
    new_height = int(new_width * img.height / img.width)
    img = img.resize((new_width, new_height), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    panel = tk.Label(frame, image=img)
    panel.image = img
    return panel


### Initialisation
   
def main():
    app = OldGloryApp()
    app.mainloop()

if __name__ == "__main__":
    main()
