import os, threading;
from utils import fileUtil, folderUtil;

class LineChunkThread(threading.Thread):
    gui=None;
    name="lineChunkThread";
    
    def __init__(self, gui):
        threading.Thread.__init__(self)
        self.gui=gui;
        
    def run(self):
        try:
            self.gui.consoleInsert("Start line chunking");
            self.gui.setAllBtnState("disabled");
            if(self.gui.saveSetting):
                while self.gui.openIndex<len(self.gui.filenames):
                    self.gui.openNextFile();
                    doLineChunk(self.gui, self.gui.lineOpt.numberOfLine);
                    self.gui.openIndex+=1;
            self.gui.openIndex=0;
            stageResult(self.gui);
            self.gui.setAllBtnState("disabled");
            self.gui.homeBtn.config(state="normal");
            self.gui.consoleInsert("Finish line chunking", "green");
        except Exception as e:
            self.gui.consoleInsert(str(e), "red");
            self.gui.setAllBtnState("normal");

def doLineChunk(gui, linesPerFile):
    file = gui.currOpenFile;
    filename = os.path.basename(file.name);
    gui.consoleInsert("do line chunk for: " + filename);
    header = file.readline();
    
    counter = 0;
    fileCounter = 1;
    fileWriter=None;
    for line in file:
        counter+=1;
        fileFullName = filename.split(".")[0] + " - " + str(fileCounter) + ".csv";
        
        if(fileWriter==None or os.path.basename(fileWriter.name)!=fileFullName):
            if(fileWriter!=None):
                fileWriter.close();
            fileWriter = fileUtil.getWriterWithHeader(fileFullName, header);
            gui.consoleInsert("File " + fileWriter.name + " was created");
        
        fileWriter.write(line);
        
        if(counter%linesPerFile==0):
            fileCounter+=1;
    gui.consoleInsert(file.name + " was successfully chunked!", "green");
    if(fileWriter!=None):
        fileWriter.close();
        
class GroupChunkThread(threading.Thread):
    gui=None;
    name="groupChunkThread";
    lastHeader="";
    
    def __init__(self, gui):
        threading.Thread.__init__(self)
        self.gui=gui;
        
    def run(self):
        pause = False;
        self.gui.consoleInsert("Start group chunking");
        try:
            self.gui.setAllBtnState("disabled");
            if(self.gui.saveSetting):
                while self.gui.openIndex<len(self.gui.filenames) and not pause:
                    self.gui.openNextFile();
                    self.gui.groupOpt.updateHeaders();
                    pause = doGroupChunk(self.gui, self);
                    if not pause:
                        self.gui.openIndex+=1;
            if not pause:
                self.gui.openIndex=0;
                stageResult(self.gui);
                self.gui.setAllBtnState("disabled");
                self.gui.homeBtn.config(state="normal");
                self.gui.consoleInsert("Finish group chunking", "green");
        except Exception as e:
            self.gui.consoleInsert(str(e), "red");
            self.gui.setAllBtnState("normal");
            
def stageResult(gui):
    folderUtil.stagingResult(gui);
    
def doGroupChunk(gui, thread):
    file = gui.currOpenFile;
    filename = os.path.basename(file.name);
    if(thread.lastHeader==""):
        thread.lastHeader = gui.groupOpt.headerRaw;
    if(thread.lastHeader!="" and thread.lastHeader!=gui.groupOpt.headerRaw):
        gui.groupOpt.updateOptionMenu();
        gui.consoleInsert(filename + " has different header!", "orange");
        gui.consoleInsert("Please adjust setting for this header and click 'start' to continue");
        thread.lastHeader = gui.groupOpt.headerRaw
        gui.setAllBtnState("normal");
        return True;
        
    index = gui.groupOpt.getHeaderIndex();
    file.readline();#skip header
    fileWriters = {};
    
    for line in file:
        groupValue = getGroupValFromLine(line, index, gui.delimiter);
        fileFullName = filename.split(".")[0] + " - " + groupValue + ".csv";
        
        if(fileWriters.get(fileFullName)==None):
            fileWriters.update({fileFullName:fileUtil.getWriterWithHeader(fileFullName, gui.groupOpt.headerRaw)});
            gui.consoleInsert("Created new file: " + fileWriters.get(fileFullName).name);
        
        fileWriters.get(fileFullName).write(line);
        
    for fw in fileWriters:
        fileWriters.get(fw).close();
    
    return False;
    
def getGroupValFromLine(line, index, delimiter):
    val = line.split(delimiter)[index].replace("/","-");
    val = val.replace("\n","");
    return val;
