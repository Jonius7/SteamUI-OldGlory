'''
custom_tk.py
Custom tk elements
- IORedirector for stdout and stderr
- ScrollFrame
- Tooltips
- Hyperlinks
'''

import tkinter as tk
from idlelib.tooltip import Hovertip, OnHoverTooltipBase

### Redirect Stdout, Stderr
### ================================
class IORedirector(object):
    '''Redirects print IO to tk.Text'''
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
### END Std Redirector


### ScrollFrame
### ================================
class ScrollFrame(tk.Frame):
    '''Modified tk.Frame to have an AutoScrollbar when needed'''
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.canvas = canvas = tk.Canvas(self, highlightthickness=0)
        canvas.grid(row=0, column=0, sticky='nsew')

        self.scroll = AutoScrollbar(self, command=self.canvas.yview, orient=tk.VERTICAL)
        self.canvas.config(yscrollcommand=self.scroll.set)
        self.scroll.grid(row=0, column=1, sticky='nsew')     

        self.content = tk.Frame(canvas)
        self.canvas.create_window(0, 0, window=self.content, anchor="nw")

        self.bind('<Configure>', self.on_configure)
        self.canvas.bind('<MouseWheel>', self.on_mousewheel)

    def on_configure(self, event):
        bbox = self.content.bbox('ALL')
        self.canvas.config(scrollregion=bbox)

    def on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def reconfigure_autoscrollbar(self):
        self.canvas.config(yscrollcommand=self.scroll.set)

class AutoScrollbar(tk.Scrollbar):
    '''Scrollbar appears when needed/text overflow'''
    def set(self, low, high): 
        if float(low) <= 0.0 and float(high) >= 1.0: 
            self.tk.call("grid", "remove", self) 
        else: 
            self.grid() 
        tk.Scrollbar.set(self, low, high)
        
    def pack(self, **kw): 
        raise (tk.TclError,"pack cannot be used with "\
        "this widget") 

    def place(self, **kw): 
        raise (tk.TclError, "place cannot be used with "\
        "this widget") 

### ================================
### END ScrollFrame

### Tooltip
### ================================
class Detail_tooltip(OnHoverTooltipBase):
    '''Hover tooltip that displays text'''
    def __init__(self, anchor_widget, text, hover_delay=1000):
        super(Detail_tooltip, self).__init__(anchor_widget, hover_delay=hover_delay)
        self.text = text
        
    def showcontents(self):
        message = tk.Message(self.tipwindow, text=self.text, justify='left',
                      background="#ffffe0", width=590, relief='solid', borderwidth=1)
        message.pack()

class Image_tooltip(OnHoverTooltipBase):
    '''Hover tooltip that displays an image'''
    def __init__(self, anchor_widget, image, hover_delay=1000):
        super(Image_tooltip, self).__init__(anchor_widget, hover_delay=hover_delay)
        self.image = image

    def showcontents(self):
        label = tk.Label(self.tipwindow, image=self.image, justify='left',
                      background="#ffffe0", width=350, relief='solid', borderwidth=1)
        label.pack()   
    
### ================================

class HyperlinkManager(object):
    """A class to easily add clickable hyperlinks to Text areas.
    Usage:
      callback = lambda : webbrowser.open("http://www.google.com/")
      text = tk.Text(...)
      hyperman = tkHyperlinkManager.HyperlinkManager(text)
      text.insert(tk.INSERT, "click me", hyperman.add(callback))
    From http://effbot.org/zone/tkinter-text-hyperlink.htm
    """
    def __init__(self, text):
        self.text = text
        self.text.tag_config("hyper", foreground="blue", underline=1)
        self.text.tag_bind("hyper", "<Enter>", self._enter)
        self.text.tag_bind("hyper", "<Leave>", self._leave)
        self.text.tag_bind("hyper", "<Button-1>", self._click)
        self.reset()

    def reset(self):
        self.links = {}

    def add(self, action):
        """Adds an action to the manager.
        :param action: A func to call.
        :return: A clickable tag to use in the text widget.
        """
        tag = "hyper-%d" % len(self.links)
        self.links[tag] = action
        return ("hyper", tag)

    def _enter(self, event):
        self.text.config(cursor="hand2")

    def _leave(self, event):
        self.text.config(cursor="")

    def _click(self, event):
        for tag in self.text.tag_names(tk.CURRENT):
            if (tag[:6] == "hyper-"):
                self.links[tag]()
                return