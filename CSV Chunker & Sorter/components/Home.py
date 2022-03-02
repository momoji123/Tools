import tkinter as tk;
from tkinter import filedialog, Listbox, Scrollbar, Frame, Button, Label;
from components.ShowMode import Mode;
from datetime import datetime;
from utils import FolderInitializer;


class HomeWindow:
    GUIRoot = None;
    master = None;
    mainContainer = None;
    fileListBox = None;
    mode = None;
    currModelLabel = None;
    console = None;
    startBtn = None;
    importFileBtn = None;
    removeBtn = None;
    chunkerBtn = None;
    sorterBtn = None;
    
    def __init__(self, master, GUIRoot):
        self.master = master;
        self.GUIRoot = GUIRoot;
        self.mainContainer = Frame(self.master);
        self.show();
        self.showTitle();
        self.initFilesManager();
        self.emptySpace(30);
        self.modeSelector();
        self.emptySpace(40);
        self.startBtn();
        self.showConsole();
        
    def showTitle(self):
        Label(self.mainContainer, justify=tk.CENTER, text="CSV Editor Tool", font="Verdana 14 bold").pack(side=tk.TOP, fill=tk.X);
        
    def initFilesManager(self):
        fileManagerContainer = Frame(self.mainContainer, bg="black", height=100);
        fileManagerContainer.pack(side=tk.TOP, fill=tk.X);
        self.prepFileList(fileManagerContainer);
        self.prepFileButtons(fileManagerContainer);
        
    def prepFileButtons(self, container):
        btnContainer = Frame(container, bg="blue", width=100);
        btnContainer.pack(side=tk.RIGHT, fill=tk.BOTH);
        
        self.importFileBtn = Button(btnContainer, text="Import Files", command=self.importFile);
        self.importFileBtn.pack(side=tk.TOP, fill=tk.BOTH, expand=True);
        self.removeBtn = Button(btnContainer, text="Remove", command=self.removeFile);
        self.removeBtn.pack(side=tk.TOP, fill=tk.BOTH, expand=True);
        
    def prepFileList(self, container):
        scrollbar = Scrollbar(container);
        
        self.fileListBox = Listbox(container, bg="white", yscrollcommand=scrollbar.set, selectmode=tk.EXTENDED);
        self.fileListBox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True);
        self.fileListBox.pack_propagate(0);
        
        scrollbar.pack(side=tk.LEFT, fill=tk.Y);
        scrollbar.config(command=self.fileListBox.yview);
        
    def importFile(self):
        filename = filedialog.askopenfilenames(initialdir="./", title="Select File", filetypes=[("CSV Files", "*.csv")]);
        for f in filename:
            self.fileListBox.insert(tk.END, f);
        self.updateStartBtn();
    
    def removeFile(self):
        filenames = self.fileListBox.curselection();
        count=0;
        for f in filenames:
            self.fileListBox.delete(f-count);
            count+=1;
        self.updateStartBtn();
    
    def modeSelector(self):
        container = Frame(self.mainContainer, bg="black", height=100);
        container.pack(side=tk.TOP, fill=tk.BOTH);
        container.pack_propagate(0);
        
        self.chunkerBtn = Button(container, text="Chunker", command= lambda : self.setMode(Mode.CHUNKER));
        self.chunkerBtn.pack(side=tk.LEFT, fill=tk.BOTH, expand=True);
        self.sorterBtn = Button(container, text="Sorter", command= lambda : self.setMode(Mode.SORTER));
        self.sorterBtn.pack(side=tk.LEFT, fill=tk.BOTH, expand=True);
        
        self.emptySpace(30);
        labelText = "Selected Mode: "+ self.mode if self.mode!=None else "None";
        self.currModelLabel = Label(self.mainContainer, justify=tk.CENTER, text = labelText, font="Verdana 14 bold");
        self.currModelLabel.pack(side=tk.TOP, fill=tk.X);
    
    def startBtn(self):
        container=Frame(self.mainContainer, bg="black", height=50);
        container.pack(side=tk.TOP, fill=tk.BOTH);
        container.pack_propagate(0);
        
        self.startBtn = Button(container, text="Start", command= lambda : self.start(), state="disabled");
        self.startBtn.pack(side=tk.LEFT, fill=tk.BOTH, expand=True);
        
    def updateStartBtn(self):
        if(self.mode!=None and self.fileListBox.size()>0):
            self.startBtn.config(state="normal");
        elif(self.startBtn["state"]=="normal"):
            self.startBtn.config(state="disabled");
            
    def start(self):
        if(self.mode==None or self.fileListBox.size()<1):
            return;
        if(self.mode==Mode.CHUNKER):
            self.GUIRoot.runChunker();
        elif(self.mode==Mode.SORTER):
            self.GUIRoot.runSorter();
    
    def setMode(self, mode):
        self.mode=mode;
        self.currModelLabel.config(text=self.mode);
        self.updateStartBtn();
    
    def emptySpace(self, height):
        Frame(self.mainContainer, height=height).pack(side=tk.TOP, fill=tk.X);
        
    def hide(self):
        self.mainContainer.place_forget();
        
    def show(self):
        self.mainContainer.place(relwidth=0.9, relheight=0.9, relx=0.05, rely=0.05);
    
    def getAllFilenames(self):
        return self.fileListBox.get(0, tk.END);
    
    def getMode(self):
        return self.mode;
    
    def showConsole(self):
        consoleContainer=Frame(self.mainContainer, bg="black", height=100);
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
            
    def setAllBtnState(self, state):
        self.startBtn.config(state=state);
        self.importFileBtn.config(state=state);
        self.removeBtn.config(state=state);
        self.chunkerBtn.config(state=state);
        self.sorterBtn.config(state=state);
    
def run(master, guiRoot):
    homeWindow = HomeWindow(master, guiRoot);
    initializerThread = FolderInitializer.Initializer(homeWindow);
    initializerThread.start();
    return homeWindow;