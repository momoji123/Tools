import tkinter as tk;
from tkinter import Toplevel, Label, Frame;

class Window:
    root = None;
    def __init__(self, root):
        self.root = root;
        self.openNew();
        
    def openNew(self):
        window = Toplevel(self.root);
        window.geometry("400x600");
        window.title("Date Pattern Info");
        Label(window, text="Days Format", font="Verdana 8 bold").pack(side=tk.TOP, pady=(20,0));
        self.addLabel(window, "Sun : %a");
        self.addLabel(window, "Sunday : %A");
        
        Label(window, text="Days Format", font="Verdana 8 bold").pack(side=tk.TOP, pady=(20,0));
        self.addLabel(window, "01 (Date) : %d");
        
        Label(window, text="Month Format", font="Verdana 8 bold").pack(side=tk.TOP, pady=(20,0));
        self.addLabel(window, "Feb : %b");
        self.addLabel(window, "February : %B");
        self.addLabel(window, "02 (Month) : %m");
        
        Label(window, text="Year Format", font="Verdana 8 bold").pack(side=tk.TOP, pady=(20,0));
        self.addLabel(window, "21 (Year) : %y");
        self.addLabel(window, "2021 : %Y");
        
        Label(window, text="Hours Format", font="Verdana 8 bold").pack(side=tk.TOP, pady=(20,0));
        self.addLabel(window, "24-Hour : %H");
        self.addLabel(window, "12-Hour: %h");
        self.addLabel(window, "Minute : %M");
        self.addLabel(window, "Second : %S");
        self.addLabel(window, "Microsecond : %f");
        
        Label(window, text="Timezone Format", font="Verdana 8 bold").pack(side=tk.TOP, pady=(20,0));
        self.addLabel(window, "+0000 : %z");
        self.addLabel(window, "UTC/GMT : %Z");
        Label(window).pack(side=tk.TOP, pady=(20,0));
        
    def addLabel(self, master, text):
        frame = Frame(master).pack(side=tk.TOP, fill=tk.BOTH, expand=True);
        Label(master, text=text).pack(side=tk.TOP, fill=tk.X);