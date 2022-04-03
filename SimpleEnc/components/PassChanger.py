import traceback
import tkinter as tk
from tkinter import Frame, Button, StringVar, Label, Entry
from cryptography.fernet import Fernet
from components import KeyGenerator


class PassChanger:
    master = None
    mainContainer = None
    fileManager = None
    console = None
    currPassInput = None
    currPass = ""
    newPassInput = None
    newPass = ""
    newPassConfInput = None
    newPassConf = ""

    def __init__(self, master, fileManager, console):
        self.master = master
        self.fileManager = fileManager
        self.console = console
        self.mainContainer = Frame(self.master)
        self.show()
        self.addEmptySpace()
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
        self.showCurrPasswordEntry(container)
        self.addEmptySpace(container, 20)
        self.showNewPasswordEntry(container)
        self.showNewPasswordConfirmEntry(container)

    def showCurrPasswordEntry(self, master):
        subContPass = Frame(master)
        subContPass.pack(side=tk.TOP, fill=tk.BOTH)
        labelPass = Label(subContPass,  anchor="w", text="Current Password: ", font="Verdana 12 bold", width=15)
        labelPass.pack(side=tk.LEFT)
        svPass = StringVar()
        svPass.trace("w", lambda name, index, mode, sv=svPass: self.setCurrPassword(sv.get()))
        self.currPassInput = Entry(subContPass, show="*", width=50, textvariable=svPass)
        self.currPassInput.pack(side=tk.LEFT)

    def setCurrPassword(self, password):
        self.currPass = password

    def showNewPasswordEntry(self, master):
        subContPass = Frame(master)
        subContPass.pack(side=tk.TOP, fill=tk.BOTH)
        labelPass = Label(subContPass, anchor="w", text="New Password: ", font="Verdana 12 bold", width=15)
        labelPass.pack(side=tk.LEFT)
        svPass = StringVar()
        svPass.trace("w", lambda name, index, mode, sv=svPass: self.setNewPassword(sv.get()))
        self.newPassInput = Entry(subContPass, show="*", width=50, textvariable=svPass)
        self.newPassInput.pack(side=tk.LEFT)

    def setNewPassword(self, password):
        self.newPass = password

    def showNewPasswordConfirmEntry(self, master):
        subContPass = Frame(master)
        subContPass.pack(side=tk.TOP, fill=tk.BOTH)
        labelPass = Label(subContPass, anchor="w", text="Confirm Password: ", font="Verdana 12 bold", width=15)
        labelPass.pack(side=tk.LEFT)
        svPass = StringVar()
        svPass.trace("w", lambda name, index, mode, sv=svPass: self.setNewPasswordConf(sv.get()))
        self.newPassConfInput = Entry(subContPass, show="*", width=50, textvariable=svPass)
        self.newPassConfInput.pack(side=tk.LEFT)

    def setNewPasswordConf(self, password):
        self.newPassConf = password

    def showStartBtn(self):
        button = Button(self.mainContainer, text="Change Password", command=self.changePassword, height=5, font="Verdana 18 bold")
        button.pack(side=tk.BOTTOM, fill=tk.BOTH)

    def changePassword(self):
        if not self.isValid():
            return
        self.console.insertProcess("Start changing password")
        try:
            decryptedByte = self.getDecryptedByte()
            encryptedByte = self.getEncryptedByte(decryptedByte)
            self.saveEncryptedByte(encryptedByte)
            self.console.insertSuccess("Password was successfully changed!")
            self.console.insertSuccess("See result here: " + self.fileManager.filePath)
        finally:
            return

    def saveEncryptedByte(self, encryptedByte):
        try:
            writer = self.fileManager.getFileWriter(path=self.fileManager.filePath, mode="wb")
            writer.write(encryptedByte)
        except Exception as e:
            traceback.print_exc()
            feedback = str(e)
            if feedback.strip() == "":
                feedback = "Failed to save file! Unknown reason"
            self.console.insertFailed(feedback)
            raise e
        finally:
            self.fileManager.closeFileWriter()

    def getEncryptedByte(self, decryptedByte):
        try:
            encryptor = Fernet(KeyGenerator.generateKey(self.newPass))
            return encryptor.encrypt(decryptedByte)
        except Exception as e:
            traceback.print_exc()
            feedback = str(e)
            if feedback.strip() == "":
                feedback = "Failed to encrypt file! Unknown reason"
            self.console.insertFailed(feedback)
            raise e

    def getDecryptedByte(self):
        try:
            reader = self.fileManager.getFileReader(mode="rb")
            encodedText = b""
            for line in reader:
                encodedText += line
            encryptor = Fernet(KeyGenerator.generateKey(self.currPass))
            return encryptor.decrypt(encodedText)
        except Exception as e:
            traceback.print_exc()
            feedback = str(e)
            if feedback.strip() == "":
                feedback = "Failed to decrpyt file! please make sure file is encrypted and current password is right."
            self.console.insertFailed(feedback)
            raise e
        finally:
            self.fileManager.closeFileReader()

    def isValid(self):
        if self.currPass.strip() == "":
            self.console.insertFailed("Current Password cannot be empty!")
            return False
        if self.newPass.strip() == "":
            self.console.insertFailed("New Password cannot be empty!")
            return False
        if self.newPass != self.newPassConf:
            self.console.insertFailed("New Password are not match!")
            return False
        return True

    def addEmptySpace(self, master=None, height=50):
        if master is None:
            master = self.mainContainer
        Frame(master, height=height).pack(side=tk.TOP, fill=tk.X)
