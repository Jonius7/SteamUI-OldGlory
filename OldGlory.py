import tkinter as tk
import tkinter.font as TkFont
from tkinter import ttk
import cssutils


    
def create_window():
    root = tk.Tk()
    
    windowW = 600
    windowH = 400
    root.geometry((str(windowW)+'x'+str(windowH)+'+950+400'))
    root.minsize(width=windowW, height=windowH)
    root.maxsize(width=windowW, height=windowH)
    
    root.iconbitmap('steam_oldglory.ico')
    root.wm_title("SteamUI-OldGlory Configurer")
    frameTitle = tk.Frame()

    ###
    default_font = TkFont.nametofont("TkDefaultFont")
    default_font.configure(size=13)

    ###
    labeltext1 = tk.StringVar()
    labeltext1.set("SteamUI-OldGlory")
    label1 = tk.Label(frameTitle, textvariable=labeltext1)
    label1.pack(padx=20)

    ###
    labeltext2 = tk.StringVar()
    labeltext2.set("A set of CSS and JS tweaks for the Steam Library")
    label2 = tk.Label(frameTitle, textvariable=labeltext2)
    label2.pack(padx=20, pady=10)

    frameCheck = tk.Frame()
    
    ###
    var1 = tk.IntVar()
    check1 = ttk.Checkbutton(frameCheck,
                             text="Install CSS Tweaks (SteamUI-OldGlory)",
                             variable=var1,
                             )
                             
    check1.bind("<Button-1>", lambda event:css_cb_check(event, var1, check2, check3))
    check1.pack()

    ###
    var2 = tk.IntVar()
    check2 = ttk.Checkbutton(frameCheck,
                             text="- Box Play Button",
                             variable=var2,
                             state='disabled')
    check2.pack()

    
    ###
    var3 = tk.IntVar()
    check3 = ttk.Checkbutton(frameCheck,
                             text="- Vertical Nav Bar",
                             variable=var3,
                             state='disabled')
    check3.pack()

    ###
    var4 = tk.IntVar()
    check4 = ttk.Checkbutton(frameCheck, text="Install with Dark Steam (steam-library)", variable=var4)
    check4.pack()
    
    frameConfirm = tk.Frame()
    ###
    button1 = ttk.Button(frameConfirm,
                       text="Install",
                       width=20,                       
    )
    button1.bind("<Button-1>", lambda event:handle_click(event, var1, labeltext2))
    button1.pack(padx=20, pady=20)


    frameTitle.pack()
    frameCheck.pack()
    frameConfirm.pack()

    
    root.mainloop()
    
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
        
def main():
    create_window()

if __name__ == "__main__":
    main()
