import tkinter as tk
from tkinter import filedialog, Listbox, Scrollbar, Frame, Button, Label
from components import FileManager, Console
from components.Mode import Mode
from components.Encryptor import Encryptor
from components.Decryptor import Decryptor


class HomeWindow:
    master = None
    mainContainer = None
    fileManager=None
    mode = None
    activeComponent = None
    console = None

    def __init__(self, master):
        self.master = master
        self.mainContainer = Frame(self.master)
        self.show()
        self.addEmptySpace()
        self.prepareFileManager()
        self.addEmptySpace()
        self.prepareModeButtons()
        self.showConsole()

    def show(self, mode=True):
        if (mode):
            self.mainContainer.place(relwidth=0.9, relheight=0.9, relx=0.05, rely=0.05)
        else:
            self.mainContainer.place_forget()

    def prepareFileManager(self):
        self.fileManager = FileManager.FileManager(self.mainContainer)
        self.fileManager.show()

    def prepareModeButtons(self):
        container = Frame(self.mainContainer, bg="black", height=30)
        container.pack(side=tk.TOP, fill=tk.X)
        container.pack_propagate(0)
        encBtn = Button(container, text="Encrypt", command=lambda: self.setMode(Mode.ENCRYPT), font="verdana 12", height=10)
        encBtn.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        decBtn = Button(container, text="Decrypt", command=lambda: self.setMode(Mode.DECRYPT), font="verdana 12", height=10)
        decBtn.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def setMode(self, mode):
        self.mode = mode
        self.renderComponentByMode()

    def addEmptySpace(self,):
        Frame(self.mainContainer, height=50).pack(side=tk.TOP, fill=tk.X)

    def renderComponentByMode(self):
        if(self.activeComponent!=None):
            self.activeComponent.show(False)
            self.activeComponent = None

        if(self.mode==Mode.ENCRYPT):
            self.activeComponent = Encryptor(self.mainContainer, self.fileManager, self.console)
        if(self.mode==Mode.DECRYPT):
            self.activeComponent = Decryptor(self.master, self.mainContainer, self.fileManager, self.console)

    def showConsole(self):
        self.console = Console.Console(self.mainContainer)


def run(master):
    home_window = HomeWindow(master)
    return home_window
