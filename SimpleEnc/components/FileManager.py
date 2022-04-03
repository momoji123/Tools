import sys
import tkinter as tk
from tkinter import filedialog, Listbox, Scrollbar, Frame, Button, Label


class FileManager:
    master = None
    mainContainer = None
    filePath = ""
    labelFilenameInfo = None
    writer = None
    reader = None

    def __init__(self, master):
        self.master = master
        self.mainContainer = Frame(self.master)
        self.initGui()
        self.autoOpenFileIfExist()

    def show(self, mode=True):
        if(mode):
            self.mainContainer.pack(side=tk.TOP, fill=tk.BOTH)
        else:
            self.mainContainer.pack_forget()

    def initGui(self):
        label = Label(self.mainContainer, text="Filename: ", font="Verdana 14 bold")
        label.pack(side=tk.LEFT, fill=tk.X)
        self.labelFilenameInfo = Label(self.mainContainer, text=self.filePath, font="Verdana 14")
        self.labelFilenameInfo.pack(side=tk.LEFT, fill=tk.X)

        button = Button(self.mainContainer, text="choose file", command=self.selectFile)
        button.pack(side=tk.RIGHT)

    def selectFile(self):
        self.filePath = filedialog.askopenfilename(initialdir="./", title="Select File",
                                                    filetypes=[("Text File", "*.txt"), ("CSV Files", "*.csv"), ("Encrypted file", "*.enc"), ("All files", "*.*")])
        self.refreshFilenameInfo()
        #self.updateStartBtn()

    def refreshFilenameInfo(self):
        self.labelFilenameInfo.config(text=self.filePath)

    def getFileWriter(self, path=None, mode="w"):
        if path is None:
            path = self.filePath
        if self.writer is not None:
            self.writer.close()
        self.writer = open(path, mode)
        return self.writer

    def getFileReader(self, path=None, mode="r"):
        if path is None:
            path = self.filePath
        if self.reader is not None:
            self.reader.close()
        self.reader = open(path, mode)
        return self.reader

    def closeFileWriter(self):
        if self.writer is not None:
            self.writer.close()

    def closeFileReader(self):
        if self.reader is not None:
            self.reader.close()

    def extractFilename(self):
        splitted = self.getSplittedPath()
        if len(splitted) < 2:
            return ""
        return splitted[len(splitted)-1]

    def extractDir(self):
        splitted = self.getSplittedPath()
        if len(splitted) < 2:
            return ""
        dir = ""
        for dirPart in splitted[0:len(splitted)-1]:
            dir += dirPart
            dir += "/"
        return dir

    def getSplittedPath(self):
        if self.filePath is None:
            return [""]
        splitted = self.filePath.split("/")
        if len(splitted) < 2:
            splitted = self.filePath.split("\\")
        if len(splitted) < 2:
            return [""]
        return splitted

    def extractExtension(self):
        filename = self.extractFilename()
        if filename == "":
            return ""
        splitted = filename.split(".")
        return splitted[len(splitted)-1]

    def autoOpenFileIfExist(self):
        if len(sys.argv)>1:
            self.filePath = sys.argv[1]
        self.refreshFilenameInfo()
