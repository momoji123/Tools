import tkinter as tk;
from tkinter import Label, Listbox, Frame, Scrollbar, Button, Entry, Canvas, Checkbutton;
from utils import fileUtil, folderUtil, SorterUtil, DatePatternUtil as dpw;
from components import SortOptions;
from datetime import datetime;
import os, time, threading;

class Sorter:
    mainGui=None;
    master=None;
    filenames=[];
    openIndex=0;
    currOpenFile=None;
    mainContainer=None;
    console=None;
    currFileLabel=None;
    currDelimiter=None;
    filename="";
    delimiter=";";
    headerRaw="";
    descending=0;
    saveSetting=True;
    startBtnCont=None;
    
    modeCheckbox=None;
    sortByOptionsCont=None;
    optionID=0;
    sortByOptions=[];
    sortByBtn=None;
    startBtn=None;
    homeBtn=None;
    
    def __init__(self, mainGui, master, filenames):
        self.mainGui = mainGui;
        self.master=master;
        self.filenames=filenames;
        self.mainContainer=Frame(self.master, bg="green");
        self.show();
        self.prepareLabels();
        self.showDelimiterSelector();
        self.showAddSortByBtn();
        self.showConsole();
        self.showStartBtn();
        self.showHomeBtn();
        self.showSortMode();
        
    def prepareLabels(self):
        self.showCurrentFile();
        self.showDelimiter();
    
    def showDelimiterSelector(self):
        container = Frame(self.mainContainer);
        container.pack(side=tk.TOP, fill=tk.X);
        
        Label(container, text="Delimiter: ").pack(side=tk.LEFT);
        self.delimiterInput = Entry(container, width=10);
        self.delimiterInput.insert(tk.END, ";");
        self.delimiterInput.pack(side=tk.LEFT);
        
        Label(container, width=5).pack(side=tk.LEFT);
        self.applyBtn = Button(container, text="Apply Delimiter", command=self.applyDelimiter);
        self.applyBtn.pack(side=tk.LEFT);
        
    def applyDelimiter(self):
        self.setCurrDelimiter(self.delimiterInput.get());
        self.removeAllOptionMenu();
        self.disableStartBtn();
    
    def removeAllOptionMenu(self):
        for opt in self.sortByOptions:
            opt.hide();
        self.sortByOptions.clear();
        
    def showCurrentFile(self):
        self.currFileLabel = Label(self.mainContainer, anchor="w", text="Current File: None", font = "Verdana 10 bold");
        self.currFileLabel.pack(side=tk.TOP, fill=tk.X);
        
    def openNextFile(self):
        self.closeCurrFile();
        if(self.openIndex<len(self.filenames)):
            self.consoleInsert("Opening next file");
            filename = self.filenames[self.openIndex];
            try:
                self.currOpenFile = fileUtil.openFile(filename, fileUtil.SOURCE_FOLDER);
                self.consoleInsert("File successfully opened");
                self.setCurrFile(filename);
            except:
                self.consoleInsert("ERROR: failed to open file: " + filename, "red");
                raise;
            return True;
        return False;
    
    def closeCurrFile(self):
        if(self.currOpenFile==None):
            return;
        self.consoleInsert("Closing currently opened file");
        self.currOpenFile.close();
        self.setCurrFile("-");
        
    def setCurrFile(self, filename):
        self.filename=filename;
        self.currFileLabel.config(text="Current File: " + self.filename);
        
    def showDelimiter(self):
        self.currDelimiter = Label(self.mainContainer, anchor="w", text="Current Delimiter: ;", font="Verdana 10");
        self.currDelimiter.pack(side=tk.TOP, fill=tk.X);
        
    def showAddSortByBtn(self):
        self.sortByBtn = Button(self.mainContainer, text="Add Sort By", font="Verdana 10", command=self.addOption);
        self.sortByBtn.pack(side=tk.TOP, fill=tk.X);
        
    def addOption(self):
        if(self.sortByOptionsCont==None):
            self.initScrollableFrame();
        sortOpt = SortOptions.SortOpt(self, self.sortByOptionsCont, self.optionID);
        self.sortByOptions.append(sortOpt);
        self.optionID += 1;
        self.enableStartBtn();
        
    def deleteOption(self, ID):
        optList = list(filter(lambda x:x.ID==ID, self.sortByOptions));
        if(len(optList)<1):
            return;
        opt = optList[0];
        opt.hide();
        self.sortByOptions.remove(opt);
        if(len(self.sortByOptions)<1):
            self.disableStartBtn();
    
    def initScrollableFrame(self):
        mainOptionFrame = Frame(self.startBtnCont);
        mainOptionFrame.pack(side=tk.TOP, fill=tk.BOTH, expand=True);
        
        canvas = Canvas(mainOptionFrame);
        self.sortByOptionsCont = Frame(canvas);
        v = Scrollbar(mainOptionFrame, command=canvas.yview);
        h = Scrollbar(mainOptionFrame, command=canvas.xview, orient=tk.HORIZONTAL);
        canvas.configure(yscrollcommand=v.set);
        canvas.configure(xscrollcommand=h.set);
        
        v.pack(side=tk.RIGHT, fill=tk.Y);
        h.pack(side=tk.BOTTOM, fill=tk.X);
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True);
        canvas.create_window((4,4), window=self.sortByOptionsCont, anchor="nw");
        self.sortByOptionsCont.bind("<Configure>", lambda event, canvas=canvas: self.onFrameConfigure(canvas));
        
    def onFrameConfigure(self, canvas):
        '''Reset the scroll region to encompass the inner frame'''
        canvas.configure(scrollregion=canvas.bbox("all"));
        
    def setCurrDelimiter(self, delimiter):
        self.delimiter = delimiter;
        self.currDelimiter.config(text="Current Delimiter: " + self.delimiter);
        
    def disableStartBtn(self):
        if(self.startBtn!=None):
            self.startBtn.config(state="disabled");
            
    def enableStartBtn(self):
        if(self.startBtn!=None):
            self.startBtn.config(state="normal");
            
    def showSortMode(self):
        self.descending = tk.IntVar();
        self.modeCheckbox = Checkbutton(self.startBtnCont, text="descending mode", variable=self.descending)
        self.modeCheckbox.pack(side=tk.TOP, fill=tk.X);
        
    def showStartBtn(self):
        if(self.startBtnCont==None):
            self.startBtnCont = Frame(self.mainContainer);
        self.startBtnCont.pack(side=tk.TOP, fill=tk.BOTH, expand=True);
        self.startBtn = Button(self.startBtnCont, text="Start", font="Verdana 10", command=self.start, height=3, state="disabled");
        self.startBtn.pack(side=tk.BOTTOM, fill=tk.X);
        
    def hideStartBtn(self):
        if(self.startBtnCont!=None):
            self.startBtnCont.pack_forget();
        self.startBtnCont=None;
        
    def showConsole(self):
        consoleContainer = Frame(self.mainContainer, bg="black", height=100);
        consoleContainer.pack(side=tk.BOTTOM, fill=tk.X);
        self.prepConsole(consoleContainer);
        
    def prepConsole(self, container):
        scrollbar = Scrollbar(container);
        self.console = Listbox(container, bg="white", yscrollcommand=scrollbar.set);
        self.console.pack(side=tk.LEFT, fill=tk.BOTH, expand=True);
        self.console.pack_propagate(0);
        scrollbar.pack(side=tk.LEFT, fill=tk.Y);
        scrollbar.config(command=self.console.yview);
        
    def consoleInsert(self, event, color=""):
        self.console.insert(tk.END, str(datetime.now()) + " " + event);
        if(color!=""):
            self.console.itemconfig(self.console.size()-1, {"fg":color});
        self.console.yview(tk.END);
        if(self.console.size()>200):
            self.console.delete(0,100);
            
    def hide(self):
        self.mainContainer.place_forget();
        
    def show(self):
        self.mainContainer.place(relwidth=0.9, relheight=0.9, relx=0.05, rely=0.05);
        
    def start(self):
        self.doSort();
        
    def doSort(self):
        runningThread=SorterUtil.Sorter(self);
        runningThread.start();
        
    def updateHeader(self):
        try:
            file=fileUtil.openFile(self.currOpenFile.name);
            self.headerRaw=file.readline();
        except Exception as e:
            self.consoleInsert("failed to read file: " + str(e), "red");
    
    def showHomeBtn(self):
        btnContainer = Frame(self.mainContainer, bg="white");
        btnContainer.pack(side=tk.BOTTOM, fill=tk.X);
        self.homeBtn = Button(btnContainer, text="Home", font = "Verdana 10", height=3, command=self.home);
        self.homeBtn.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True);
        
    def home(self):
        self.closeCurrFile();
        self.removeAllOptionMenu();
        self.hide();
        self.mainGui.home.show();
        
    def openDatePatternWindow(self):
        dpw.Window(self.mainGui.root);
        
    def setAllBtnState(self, state):
        self.startBtn.config(state=state);
        self.homeBtn.config(state=state);
        self.sortByBtn.config(state=state);
        self.applyBtn.config(state=state);
        for opt in self.sortByOptions:
            opt.setInputsState(state);
        self.modeCheckbox.config(state=state);
        
class Initializer(threading.Thread):
    mainGui=None;
    home=None;
    root=None;
    filenames=[];
    
    def __init__(self, mainGui, root, filenames):
        threading.Thread.__init__(self)
        self.home=mainGui.home;
        self.mainGui = mainGui;
        self.root = root;
        self.filenames = filenames;
    
    def run(self):
        try:
            self.mainGui.home.setAllBtnState("disabled");
            folderUtil.clearTempFolder(self.home);
            folderUtil.backupFiles(self.home, self.filenames);
            folderUtil.clearResultFolder(self.home);
            self.mainGui.home.hide();
            self.mainGui.home.console.delete(0, tk.END);
            self.mainGui.home.setAllBtnState("normal");
            self.mainGui.home.updateStartBtn();
            sorter = Sorter(self.mainGui, self.root, self.filenames);
            sorter.openNextFile();
        except Exception as e:
            gui.consoleInsert(str(e), "red");
            raise e;
        finally:
            self.mainGui.home.setAllBtnState("normal");
            self.mainGui.home.updateStartBtn();

def run(mainGui, root, filenames):
    sorterInitializer = Initializer(mainGui, root, filenames);
    sorterInitializer.start();