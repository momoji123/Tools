import sys;
import os, sys, traceback;
from components import GUIManager;

def main():
    GUIManager.start();

if __name__=="__main__":
    try:
        main()
    except:
        traceback.print_exc();
    finally:
        sys.exit();