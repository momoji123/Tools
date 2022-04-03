import tkinter as tk
from tkinter import Toplevel, Frame, Scrollbar, Text, Button
from components import Console, KeyGenerator
from cryptography.fernet import Fernet


class Window:
    root = None
    mainContainer = None
    result = None
    fileDir = ""
    filename = ""
    console = None
    text = None
    password = ""

    def __init__(self, root, result:str, fileManager, password):
        self.password = password
        self.root = root
        self.result = result.strip()
        self.fileDir = fileManager.extractDir()
        self.filename = fileManager.extractFilename().replace(".enc", "")
        self.openNew()
        self.showTextResult()
        self.showBtnMenu()
        self.showConsole()

    def openNew(self):
        window = Toplevel(self.root)
        window.geometry("800x600")
        self.mainContainer = Frame(window, padx=5, pady=5, width=100, height=100)
        self.mainContainer.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky=tk.E+tk.W+tk.N+tk.S)

        window.columnconfigure(0, weight=1)
        window.rowconfigure(1, weight=1)

        self.mainContainer.rowconfigure(0, weight=1)
        self.mainContainer.columnconfigure(0, weight=1)

    def showTextResult(self):
        textContainer = Frame(self.mainContainer)
        textContainer.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        S = Scrollbar(textContainer)
        self.text = Text(textContainer, height=4, width=50)
        S.pack(side=tk.RIGHT, fill=tk.Y)
        self.text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        S.config(command=self.text.yview)
        self.text.config(yscrollcommand=S.set)
        self.text.insert(tk.END, self.result)

    def showBtnMenu(self):
        btnContainer = Frame(self.mainContainer, bg="black")
        btnContainer.pack(side=tk.TOP, fill=tk.X)
        saveOrBtn = Button(btnContainer, text="Save Original (Plain)", command=self.savePlain, font="Verdana 15")
        saveOrBtn.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        saveChBtn = Button(btnContainer, text="Save Changed (Plain)", command=self.saveChangedPlain, font="Verdana 15")
        saveChBtn.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        saveChEncBtn = Button(btnContainer, text="Save Changed (Enc)", command=self.saveChangedEnc, font="Verdana 15")
        saveChEncBtn.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def showConsole(self):
        self.console = Console.Console(self.mainContainer)

    def saveChangedPlain(self):
        self.result = self.text.get("1.0", tk.END)
        self.savePlain()

    def savePlain(self):
        targetFilePath = self.fileDir + self.filename
        self.console.insertProcess("saving file to: " + targetFilePath)
        writer = None
        try:
            writer = open(targetFilePath, "w")
            writer.write(self.result)
            self.console.insertSuccess("File was successfully saved!")
            self.console.insertSuccess("see file here: " + targetFilePath)
        except Exception as e:
            self.console.insertFailed("failed saving file! " + str(e))
        finally:
            if writer is not None:
                writer.close()

    def saveChangedEnc(self):
        self.result = self.text.get("1.0", tk.END)
        self.saveEnc()

    def saveEnc(self):
        targetFilePath = self.fileDir + self.filename + ".enc"
        self.console.insertProcess("saving file to: " + targetFilePath)
        writer = None
        try:
            key = KeyGenerator.generateKey(self.password)
            textBin = self.result.encode()
            encryptor = Fernet(key)
            encryptedText = encryptor.encrypt(textBin)
            writer = open(targetFilePath, "wb")
            writer.write(encryptedText)
            self.console.insertSuccess("File was successfully saved & encrypted!")
        except Exception as e:
            self.console.insertFailed("failed saving file! " + str(e))
        finally:
            if writer is not None:
                writer.close()
