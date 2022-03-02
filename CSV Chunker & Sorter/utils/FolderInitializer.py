import threading;
from utils import folderUtil;

class Initializer(threading.Thread):
    gui=None;
    
    def __init__(self, gui):
        threading.Thread.__init__(self)
        self.gui=gui;
        
    def run(self):
        self.gui.consoleInsert("Initializing");
        try:
            self.gui.setAllBtnState("disabled");
            folderUtil.clearStagingFolder(self.gui);
            self.gui.setAllBtnState("normal");
            self.gui.updateStartBtn();
            self.gui.consoleInsert("Initialization completed!", "green");
        except Exception as e:
            self.gui.consoleInsert(str(e) + ". Please restart program", "red");
            raise e;