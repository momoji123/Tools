import threading, os, functools
from utils import fileUtil, folderUtil;
from components.SortOptions import DataType;
from collections import deque;
from datetime import datetime;

class SortObj:
    param = [];
    value = "";
    
    def __init__(self, param, value):
        self.param = param;
        self.value = value;

class Sorter(threading.Thread):
    gui=None;
    name="sorter";
    lastHeader="";
    
    def __init__(self, gui):
        threading.Thread.__init__(self)
        self.gui=gui;
        
    def run(self):
        pause = False;
        err = False;
        self.gui.consoleInsert("Start Sorting");
        try:
            self.gui.setAllBtnState("disabled");
            if(self.gui.saveSetting):
                while self.gui.openIndex<len(self.gui.filenames) and not pause:
                    self.gui.openNextFile();
                    self.gui.updateHeader();
                    pause = doSort(self.gui, self);
                    if not pause:
                        self.gui.openIndex+=1;
            if not pause:
                self.gui.openIndex=0;
                self.gui.openNextFile();
                self.gui.removeAllOptionMenu();
                folderUtil.stagingResult(self.gui);
                self.gui.consoleInsert("Finish sorting file", "green");
        except Exception as e:
            self.gui.consoleInsert(str(e), "red");
            err = True;
        finally:
            if err or pause:
                self.gui.setAllBtnState("normal");
            if pause:
                self.gui.disableStartBtn();
            self.gui.homeBtn.config(state="normal");
        
def doSort(gui, thread):
    if(thread.lastHeader==""):
        thread.lastHeader = gui.headerRaw;
    if(thread.lastHeader!=gui.headerRaw):
        gui.removeAllOptionMenu();
        gui.consoleInsert(gui.filename + " has different header!", "orange");
        gui.consoleInsert("Please adjust setting for this header and click 'start' to continue");
        return True;
    
    file = gui.currOpenFile;
    filename = os.path.basename(file.name);
    
    gui.consoleInsert("Preparing parameters", "blue");
    objContainer = [];
    gui.currOpenFile.readline()#skip header
    for line in gui.currOpenFile:
        objContainer.append(SortObj(getParams(gui, line), line));
        
    gui.consoleInsert("Start sorting", "blue");
    objContainer.sort(key=functools.cmp_to_key(compareSortObj), reverse= gui.descending.get());
    
    gui.consoleInsert("Saving..", "blue");
    objContainer = deque(objContainer);
    fileWriter = fileUtil.getWriterWithHeader(filename, thread.lastHeader);
    try:
        while objContainer:
            fileWriter.write(objContainer.popleft().value);
        gui.consoleInsert(filename + " was successfully sorted", "green");
    except Exception as e:
        gui.consoleInsert("Failed to write file: " + filename + " " + str(e), "red");
        raise e;
    finally:
        if fileWriter!=None:
            fileWriter.close();
    return False;

def compareSortObj(obj1, obj2):
    result = 0;
    for i in range(len(obj1.param)):
        cmp1 = obj1.param[i];
        cmp2 = obj2.param[i];
        
        if(type(cmp1)==str):
            result = directCompare(cmp1.lower(), cmp2.lower());
        else:
            result = directCompare(cmp1, cmp2);
        if(result!=0):
            return result;
    return result;
    
def directCompare(num1, num2):
    if(num1==num2):
        return 0;
    if(num1<num2):
        return -1;
    return 1;

def getParams(gui, line):
    splitLine = line.split(gui.delimiter);
    params=[];
    for opt in gui.sortByOptions:
        value = splitLine[opt.headerIdx];
        if(opt.dataType==DataType.NUMBER):
            params.append(getNumber(value));
            continue;
        if(opt.dataType==DataType.DATETIME):
            params.append(getDate(value, opt.datePattern));
            continue;
        params.append(value);
    return params;
    
def getDate(value, pattern):
    if(value==""):
        return datetime.min;
    return datetime.strptime(value, pattern);

def getNumber(value):
    if(value==None or value==""):
        return 0.0;
    return float(value);