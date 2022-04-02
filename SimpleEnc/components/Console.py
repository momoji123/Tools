import tkinter as tk
from tkinter import Scrollbar, Listbox, Frame
from datetime import datetime

class Console:
    master = None
    mainContainer = None
    console = None

    def __init__(self, master):
        self.master = master
        self.mainContainer = Frame(self.master)
        self.mainContainer.pack(side=tk.BOTTOM, fill=tk.BOTH)
        self.showConsole()

    def showConsole(self):
        consoleContainer = Frame(self.mainContainer, bg="black", height=100)
        consoleContainer.pack(side=tk.BOTTOM, fill=tk.X)
        self.prepConsole(consoleContainer)

    def prepConsole(self, container):
        scrollbar = Scrollbar(container)
        self.console = Listbox(container, bg="white", yscrollcommand=scrollbar.set)
        self.console.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.console.pack_propagate(0)
        scrollbar.pack(side=tk.LEFT, fill=tk.Y)
        scrollbar.config(command=self.console.yview)

    def consoleInsert(self, event, color=""):
        self.console.insert(tk.END, event)
        if (color != ""):
            self.console.itemconfig(self.console.size() - 1, {"fg": color})
        self.console.yview(tk.END)
        if (self.console.size() > 200):
            self.console.delete(0, 100)

    def clear(self):
        self.console.delete(0)

    def insertProcess(self, event):
        self.consoleInsert(str(datetime.now()) + " " + event, "blue")

    def insertSuccess(self, event):
        self.consoleInsert(str(datetime.now()) + " " + event, "green")

    def insertWarn(self, event):
        self.consoleInsert(str(datetime.now()) + " " + event, "orange")

    def insertFailed(self, event):
        self.consoleInsert(str(datetime.now()) + " " + event, "red")
