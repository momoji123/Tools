import tkinter as tk;
from tkinter import Frame, Button, OptionMenu, StringVar, Label, Entry;
from utils import fileUtil;

class DataType:
    NUMBER="number";
    STRING="string";
    DATETIME="datetime";
    
    def getList():
        return [DataType.NUMBER, DataType.STRING, DataType.DATETIME];
        
class SortOpt:
    ID=0;
    sorterGui=None;
    mainContainer=None;
    headers=[];
    selectedHeader="";
    headerIdx=0;
    dataType=DataType.NUMBER;
    datePattern="";
    
    selectedGroup=None;
    groupMenu=None;
    
    selectedTyp=None;
    typMenu=None;
    
    cancelBtn=None;
    
    datePatternInputCont=None;
    dateEntry=None;
    
    def __init__(self, sorterGui, master, ID):
        self.ID=ID;
        self.sorterGui = sorterGui;
        self.mainContainer = Frame(master, height=30, width=850);
        self.show();
        self.getHeader();
        self.showOptions();
        self.showCancelBtn();
        
    def show(self):
        self.mainContainer.pack(side=tk.TOP, fill=tk.X, expand=True);
        self.mainContainer.config(width=850);
    
    def hide(self):
        self.mainContainer.pack_forget();
    
    def showOptions(self):
        try:
            self.showHeaderSelector();
            self.showTypeSelector();
        except Exception as e:
            self.sorterGui.consoleInsert("failed to show options: " + str(e), "red");
            
    def showCancelBtn(self):
        self.cancelBtn = Button(self.mainContainer, text="X", bg="red", fg="black", command=self.cancel);
        self.cancelBtn.pack(side=tk.RIGHT);
        Label(self.mainContainer, width=3).pack(side=tk.RIGHT, fill=tk.X, expand=True);
        
    def cancel(self):
        self.sorterGui.deleteOption(self.ID);
    
    def getHeader(self):
        if(self.sorterGui.headerRaw==""):
            self.sorterGui.updateHeader();
        try:
            self.headers = self.sorterGui.headerRaw.split(self.sorterGui.delimiter);
        except Exception as e:
            self.sorterGui.consoleInsert("failed to split raw header: " + str(e), "red");
            self.headers=[];
    
    def showHeaderSelector(self):
        selectorCont = Frame(self.mainContainer, bg="black", height=50);
        selectorCont.pack(side=tk.LEFT);
        
        Label(selectorCont, text="Header: ").pack(side=tk.LEFT, fill=tk.Y);
        self.selectedGroup = StringVar(selectorCont);
        self.selectedGroup.set(self.headers[0]);
        self.groupMenu = OptionMenu(selectorCont, self.selectedGroup, *self.headers, command=self.selectHeader);
        self.groupMenu.pack(side=tk.LEFT, fill=tk.Y);
        
    def selectHeader(self, selection):
        self.selectedHeader=selection;
        self.headerIdx = self.headers.index(selection);
        
    def showTypeSelector(self):
        selectorCont = Frame(self.mainContainer, bg="black", height=50);
        selectorCont.pack(side=tk.LEFT);
        
        types = DataType.getList();
        
        Label(selectorCont, text="Header: ").pack(side=tk.LEFT, fill=tk.Y);
        self.selectedTyp = StringVar(selectorCont);
        self.selectedTyp.set(types[0]);
        self.typMenu = OptionMenu(selectorCont, self.selectedTyp, *types, command=self.selectType);
        self.typMenu.pack(side=tk.LEFT, fill=tk.Y);
        
    def selectType(self, selection):
        self.dataType = selection;
        if(selection==DataType.DATETIME):
            self.showDatePattern(True);
            return;
        self.showDatePattern(False);
        
    def showDatePattern(self, show):
        if not show:
            if(self.datePatternInputCont==None):
                return;
            self.datePatternInputCont.pack_forget();
            return;
        newInput = self.datePatternInputCont==None;
        if(newInput):
            self.datePatternInputCont = Frame(self.mainContainer, bg="white");
        self.datePatternInputCont.pack(side=tk.LEFT, fill=tk.BOTH);
        
        if not newInput:
            return;
        
        Label(self.datePatternInputCont, text="Date Pattern: ").pack(side=tk.LEFT, fill=tk.BOTH);
        sv=StringVar();
        sv.trace("w", lambda name, index, mode, sv=sv: self.setDatePattern(sv));
        self.dateEntry = Entry(self.datePatternInputCont, textvariable=sv);
        self.dateEntry.pack(side=tk.LEFT, fill=tk.BOTH);
        Button(self.datePatternInputCont, text="?", command=self.showDatePatternWindow).pack(side=tk.LEFT, fill=tk.BOTH);
        
    def showDatePatternWindow(self):
        self.sorterGui.openDatePatternWindow();
        
    def setDatePattern(self, stringvar):
        self.datePattern = stringvar.get();
        
    def setInputsState(self, state):
        if(self.dateEntry!=None):
            self.dateEntry.config(state=state);
        self.cancelBtn.config(state=state);
        self.typMenu.config(state=state);
        self.groupMenu.config(state=state);