import tkinter as tk;
from components import Home, ChunkerGui as cgui, SorterGui as sgui;
from utils import folderUtil;
import os, sys, traceback;

class GUIRoot:
    root=None;
    home=None;
    
    def __init__(self):
        self.root = tk.Tk();
        self.root.title("CSV Editor Tool");
        background = tk.Canvas(self.root, width=1000, height=800);
        background.pack();
        self.runHome(self.root);
        self.root.mainloop();
        
    def runHome(self, master):
        if(self.home==None):
            self.home = Home.run(master, self);
            
    def runChunker(self):
        filenames = self.home.getAllFilenames();
        cgui.run(self, self.root, filenames);
        
    def runSorter(self):
        filenames = self.home.getAllFilenames();
        sgui.run(self, self.root, filenames);

def main():
    root = GUIRoot();

if __name__ == "__main__":
    try:
        main();
    except:
        traceback.print_exc();
    finally:
        sys.exit();