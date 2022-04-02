import tkinter as tk
from tkinter import filedialog, Listbox, Scrollbar, Frame, Button, Label, Entry, StringVar
from cryptography.fernet import Fernet
from components import KeyGenerator
import traceback


class Encryptor:
    master = None
    mainContainer = None
    console = None
    fileManager = None
    passInput = None
    confPassInput = None
    password = ""
    confPassword = ""

    def __init__(self, master, fileManager, console):
        self.fileManager = fileManager
        self.master = master
        self.mainContainer = Frame(self.master)
        self.console = console
        self.show()
        self.showPasswordInput()
        self.addEmptySpace()
        self.showStartBtn()

    def show(self, mode=True):
        if(mode):
            self.mainContainer.pack(side=tk.TOP, fill=tk.BOTH)
        else:
            self.mainContainer.pack_forget()

    def showPasswordInput(self):
        container = Frame(self.mainContainer, bg="black")
        container.pack(side=tk.TOP, fill=tk.BOTH)
        self.showPasswordEntry(container)
        self.showConfirmPasswordEntry(container)

    def showPasswordEntry(self, master):
        subContPass = Frame(master)
        subContPass.pack(side=tk.TOP, fill=tk.BOTH)
        labelPass = Label(subContPass,  anchor="w", text="Password: ", font="Verdana 12 bold", width=15)
        labelPass.pack(side=tk.LEFT)
        svPass = StringVar()
        svPass.trace("w", lambda name, index, mode, sv=svPass: self.setPassword(sv.get()))
        self.passInput = Entry(subContPass, show="*", width=50, textvariable=svPass)
        self.passInput.pack(side=tk.LEFT)

    def setPassword(self, input):
        self.password = input

    def showConfirmPasswordEntry(self, master):
        subContPass = Frame(master)
        subContPass.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        labelPass = Label(subContPass, anchor="w", text="Confirm Password: ", font="Verdana 12 bold", width=15)
        labelPass.pack(side=tk.LEFT)
        svPass = StringVar()
        svPass.trace("w", lambda name, index, mode, sv=svPass: self.setConfPassword(sv.get()))
        self.confPassInput = Entry(subContPass, show="*", width=50, textvariable=svPass)
        self.confPassInput.pack(side=tk.LEFT)

    def setConfPassword(self, input):
        self.confPassword = input

    def showStartBtn(self):
        button = Button(self.mainContainer, text="Start Encrypt", command=self.startEncrypt, height=5, font="Verdana 18 bold")
        button.pack(side=tk.BOTTOM, fill=tk.BOTH)

    def startEncrypt(self):
        if self.password.strip() == "":
            self.console.insertFailed("Password cannot be empty!")
            return
        if self.password != self.confPassword:
            self.console.insertFailed("Password are not match!")
            return
        self.console.insertProcess("Start encrypting file")
        try:
            reader = self.fileManager.getFileReader()
            text = ""
            for line in reader:
                text+=line
            encodedText = text.encode()
            encryptor = Fernet(KeyGenerator.generateKey(self.password))
            encryptedText = encryptor.encrypt(encodedText)
            targetDir = self.fileManager.extractDir() + self.fileManager.extractFilename() + "_enc"
            writer = self.fileManager.getFileWriter(path=targetDir, mode="wb")
            writer.write(encryptedText)
            self.console.insertSuccess("File was successfully encrypted!")
            self.console.insertSuccess("See result here: " + targetDir)
        except Exception as e:
            traceback.print_exc()
            self.console.insertFailed(str(e))
        finally:
            self.fileManager.closeFileReader()
            self.fileManager.closeFileWriter()

    def addEmptySpace(self):
        Frame(self.mainContainer, height=50).pack(side=tk.TOP, fill=tk.X)
