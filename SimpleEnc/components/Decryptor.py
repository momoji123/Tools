import tkinter as tk
from tkinter import Frame, Button, Label, Entry, StringVar
from cryptography.fernet import Fernet
from components import KeyGenerator, ResultWindow
import traceback


class Decryptor:
    root = None
    master = None
    mainContainer = None
    console = None
    fileManager = None
    passInput = None
    password = ""
    result = ""

    def __init__(self, root, master, fileManager, console):
        self.root = root
        self.fileManager = fileManager
        self.master = master
        self.mainContainer = Frame(self.master)
        self.console = console
        self.show()
        self.showPasswordInput()
        self.addEmptySpace()
        self.showStartBtn()

    def show(self, mode=True):
        if mode:
            self.mainContainer.pack(side=tk.TOP, fill=tk.BOTH)
        else:
            self.mainContainer.pack_forget()

    def showPasswordInput(self):
        container = Frame(self.mainContainer, bg="black")
        container.pack(side=tk.TOP, fill=tk.BOTH)
        self.showPasswordEntry(container)

    def showPasswordEntry(self, master):
        subContPass = Frame(master)
        subContPass.pack(side=tk.TOP, fill=tk.BOTH)
        labelPass = Label(subContPass,  anchor="w", text="Password: ", font="Verdana 12 bold", width=15)
        labelPass.pack(side=tk.LEFT)
        svPass = StringVar()
        svPass.trace("w", lambda name, index, mode, sv=svPass: self.setPassword(sv.get()))
        self.passInput = Entry(subContPass, show="*", width=50, textvariable=svPass)
        self.passInput.pack(side=tk.LEFT)

    def setPassword(self, password):
        self.password = password

    def showStartBtn(self):
        button = Button(self.mainContainer, text="Start Decrpyt", command=self.startDecrypt, height=5, font="Verdana 18 bold")
        button.pack(side=tk.BOTTOM, fill=tk.BOTH)

    def startDecrypt(self):
        self.console.insertProcess("Start decrypting file")
        try:
            reader = self.fileManager.getFileReader(mode="rb")
            textBin = b""
            for line in reader:
                textBin += line
            encodedText = textBin
            encryptor = Fernet(KeyGenerator.generateKey(self.password))
            encryptedText = encryptor.decrypt(encodedText)
            self.result = encryptedText.decode()
            self.showResult()
            self.console.insertSuccess("File was successfully decrypted!")
        except Exception as e:
            traceback.print_exc()
            if str(e) == "":
                self.console.insertFailed("Failed to encrypt file! please make sure opened file is encrypted file and password is right")
            else:
                self.console.insertFailed(str(e))
        finally:
            self.fileManager.closeFileReader()
            self.fileManager.closeFileWriter()

    def showResult(self):
        ResultWindow.Window(self.root, self.result, self.fileManager, self.password)

    def addEmptySpace(self):
        Frame(self.mainContainer, height=50).pack(side=tk.TOP, fill=tk.X)
