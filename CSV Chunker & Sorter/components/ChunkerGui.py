import tkinter as tk;
from tkinter import Label, Listbox, Frame, Scrollbar, Button;
from utils import ChunkerUtil, folderUtil, fileUtil;
from utils.ChunkMode import Mode;
from components import LineOptions as lineOpt, GroupOptions as groupOpt;
from datetime import datetime;
import os, time, threading;

class Chunker:
    mainGui=None;
    master=None;
    filenames=[];
    openIndex = 0;
    currOpenFile=None;
    mainContainer=None;
    console=None;
    currFileLabel=None;
    currDelimiter=None;
    currChunkMode=None;
    filename="";
    delimiter=";";
    mode="";
    chunkInfo="";
    saveSetting=True;
    startBtnCont=None;
    lineOpt=None;
    groupOpt=None;
    
    lineBtn=None;
    groupBtn=None;
    startBtn=None;
    homeBtn=None;
    
    def __init__(self, mainGui, master, filenames):
        self.mainGui = mainGui;
        self.master = master;
        self.filenames = filenames;
        self.mainContainer = Frame(self.master);
        self.show();
        self.prepareLabels();
        self.showModeSelector();
        self.showConsole();
        self.showHomeBtn();
    
    def prepareLabels(self):
        self.showCurrentFile();
        self.showDelimiter();
        self.showChunkMode();
        
    def showCurrentFile(self):
        self.currFileLabel = Label(self.mainContainer, anchor="w", text="Current File: None", font="Verdana 10 bold");
        self.currFileLabel.pack(side=tk.TOP, fill=tk.X);
        
    def openNextFile(self):
        self.closeCurrFile();
        self.consoleInsert("Opening next file");
        if(self.openIndex<len(self.filenames)):
            filename = self.filenames[self.openIndex];
            try:
                self.currOpenFile = fileUtil.openFile(filename, fileUtil.SOURCE_FOLDER);
                self.consoleInsert("File Successfully opened");
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
        
    def setCurrDelimiter(self, delimiter):
        self.delimiter = delimiter;
        self.currDelimiter.config(text="Current Delimiter: " + self.delimiter);
        
    def showChunkMode(self):
        self.currChunkMode = Label(self.mainContainer, anchor="w", text="Chunk mode: None", font="Verdana 10");
        self.currChunkMode.pack(side=tk.TOP, fill=tk.X);
        
    def setChunkMode(self, mode):
        self.mode = mode;
        self.currChunkMode.config(text = "Chunk mode: " + self.mode);
    
    def showModeSelector(self):
        btnContainer = Frame(self.mainContainer, bg="black", height=100);
        btnContainer.pack(side=tk.TOP, fill=tk.X);
        self.lineBtn = Button(btnContainer, text="Lines", command= lambda : self.selectMode(Mode.LINES));
        self.lineBtn.pack(side=tk.LEFT, fill=tk.BOTH, expand=True);
        self.groupBtn = Button(btnContainer, text="Group", command= lambda : self.selectMode(Mode.GROUP));
        self.groupBtn.pack(side=tk.LEFT, fill=tk.BOTH, expand=True);
        
    def selectMode(self, mode):
        self.setChunkMode(mode);
        self.hideStartBtn();
        if(mode==Mode.LINES):
            if(self.groupOpt!=None):
                self.groupOpt.hide();
            if(self.lineOpt!=None):
                self.lineOpt.show();
            else:
                self.lineOpt = lineOpt.LineOptions(self);
            self.showStartBtn();
        elif(mode==Mode.GROUP):
            if(self.lineOpt!=None):
                self.lineOpt.hide();
            if(self.groupOpt!=None):
                self.groupOpt.show();
            else:
                self.groupOpt = groupOpt.GroupOptions(self);
            self.showStartBtn();
            self.enableStartBtn();
            
    def disableStartBtn(self):
        if(self.startBtn!=None):
            self.startBtn.config(state="disabled");
    
    def enableStartBtn(self):
        if(self.startBtn!=None):
            self.startBtn.config(state="normal");
    
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
        self.doChunk();
    
    def doChunk(self):
        if(self.mode==Mode.LINES):
            runningThread = ChunkerUtil.LineChunkThread(self);
            runningThread.start();
        if(self.mode==Mode.GROUP):
            runningThread = ChunkerUtil.GroupChunkThread(self);
            runningThread.start();
            
    def showHomeBtn(self):
        btnContainer = Frame(self.mainContainer, bg="white");
        btnContainer.pack(side=tk.BOTTOM, fill=tk.X);
        self.homeBtn = Button(btnContainer, text="Home", font="Verdana 10", height=3, command=self.home);
        self.homeBtn.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True);
    
    def home(self):
        self.closeCurrFile();
        self.hide();
        self.mainGui.home.show();
        
    def setAllBtnState(self, state):
        self.lineBtn.config(state=state);
        self.groupBtn.config(state=state);
        self.startBtn.config(state=state);
        self.homeBtn.config(state=state);
        if(self.mode==Mode.LINES):
            self.lineOpt.setAllBtnState(state);
        if(self.groupOpt!=None):
            self.groupOpt.setAllBtnState(state);
            
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
            chunker = Chunker(self.mainGui, self.root, self.filenames);
            chunker.openNextFile();
        except Exception as e:
            gui.consoleInsert(str(e), "red");
            raise e;
        finally:
            self.mainGui.home.setAllBtnState("normal");
            self.mainGui.home.updateStartBtn();

def run(mainGui, root, filenames):
    chunkerInitializer = Initializer(mainGui, root, filenames);
    chunkerInitializer.start();