import tkinter as tk;
from tkinter import Label, Frame, Entry, Button, StringVar, OptionMenu;
from utils import ChunkerUtil, fileUtil;

DEFAULT_SELECTION = "Select Group By"

class GroupOptions:
    chunkerGUI = None;
    master = None;
    mainContainer = None;
    headerRaw="";
    headers = [DEFAULT_SELECTION];
    selectedGroup=None;
    optionMenu=None;
    delimiterInput=None;
    
    applyBtn=None;
    
    def __init__(self, chunkerGUI):
        self.chunkerGUI = chunkerGUI;
        self.master = chunkerGUI.mainContainer;
        self.mainContainer = Frame(self.master);
        self.show();
        self.showOptions();
        self.chunkerGUI.enableStartBtn();
        
    def showOptions(self):
        self.showHeaderSelector();
        self.showDelimiterSelector();
        
    def showHeaderSelector(self):
        topCont = Frame(self.mainContainer);
        topCont.pack(side=tk.TOP, fill=tk.X);
        selectorCont = Frame(topCont, width=800, height=50);
        selectorCont.pack(side=tk.LEFT);
        selectorCont.pack_propagate(0);
        
        Label(selectorCont, text="Group by: ").pack(side=tk.LEFT, fill=tk.Y);
        self.selectedGroup = StringVar(selectorCont);
        self.optionMenu = OptionMenu(selectorCont, self.selectedGroup, *self.headers);
        self.optionMenu.pack(side=tk.LEFT, fill=tk.Y);
        self.updateOptionMenu();
    
    def showDelimiterSelector(self):
        container = Frame(self.mainContainer);
        container.pack(side=tk.TOP, fill=tk.X);
        
        Label(container, text="Delimiter: ").pack(side=tk.LEFT);
        self.delimiterInput = Entry(container, width=10);
        self.delimiterInput.insert(tk.END, ";");
        self.delimiterInput.pack(side=tk.LEFT);
        self.applyBtn = Button(container, text="Apply Delimiter", command=self.applyDelimiter);
        self.applyBtn.pack(side=tk.LEFT, padx=(20,0));
        
    def applyDelimiter(self):
        self.chunkerGUI.setCurrDelimiter(self.delimiterInput.get());
        self.updateOptionMenu();
        
    def updateOptionMenu(self):
        self.updateHeaders();
        menu = self.optionMenu["menu"];
        menu.delete(0, tk.END);
        for string in self.headers:
            menu.add_command(label=string, command=lambda value=string: self.selectedGroup.set(value));
        self.selectedGroup.set(self.headers[0]);
        
    def updateHeaders(self):
        filename=self.chunkerGUI.filenames[self.chunkerGUI.openIndex];
        f = fileUtil.openFile(filename, fileUtil.SOURCE_FOLDER);
        firstLine = f.readline();
        self.headerRaw = firstLine;
        self.headers = firstLine.split(self.chunkerGUI.delimiter);
        f.close();
        
    def getHeaderIndex(self):
        return self.headers.index(self.selectedGroup.get());
        
    def show(self):
        self.mainContainer.pack(fill=tk.BOTH, side=tk.TOP);
        
    def hide(self):
        self.mainContainer.pack_forget();
    
    def setAllBtnState(self, state):
        self.applyBtn.config(state=state);
        self.optionMenu.config(state=state);