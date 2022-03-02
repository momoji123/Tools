import tkinter as tk;
from tkinter import Label, Frame, Entry, Button, StringVar;

class LineOptions:
    chunkerGUI=None;
    master=None;
    mainContainer=None;
    numberOfLine=None;
    feedbackLabel=None;
    linesEntry=None;
    
    def __init__(self, chunkerGUI):
        self.chunkerGUI = chunkerGUI;
        self.master = chunkerGUI.mainContainer;
        self.mainContainer = Frame(self.master);
        self.show();
        self.showOptions();
        self.updateStartBtn();
        
    def showOptions(self):
        Label(self.mainContainer, anchor="w", text="Lines per chunk: ", font="Verdana 10").pack(side=tk.LEFT, fill=tk.BOTH);
        sv=StringVar();
        sv.trace("w", lambda name, index, mode, sv=sv: self.apply(sv.get()));
        self.linesEntry = Entry(self.mainContainer, textvariable=sv);
        self.linesEntry.pack(side=tk.LEFT, fill=tk.BOTH);
        
    def apply(self, linesInput):
        self.chunkerGUI.disableStartBtn();
        lines = None;
        try:
            lines = int(linesInput);
            self.numberOfLine = lines;
            self.showFeedback("Successfully applied!", "green");
        except:
            self.showFeedback("Please input only numbers", "red");
            self.numberOfLine = None;
        if(lines!=None and lines<=0):
            self.numberOfLine = None;
            self.showFeedback("Line must bigger than zero", "red");
        self.updateStartBtn();
    
    def updateStartBtn(self):
        if(self.numberOfLine!=None):
            self.chunkerGUI.enableStartBtn();
        else:
            self.chunkerGUI.disableStartBtn();
    
    def showFeedback(self, text, color):
        if(self.feedbackLabel==None):
            self.feedbackLabel = Label(self.mainContainer, anchor="w", font="Verdana 8");
            self.feedbackLabel.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True);
        self.feedbackLabel.config(text=text);
        self.feedbackLabel.config(fg=color);
        
    def hide(self):
        self.mainContainer.pack_forget();
    
    def show(self):
        self.mainContainer.pack(fill=tk.BOTH, side=tk.TOP);
        
    def setAllBtnState(self, state):
        self.linesEntry.config(state=state);