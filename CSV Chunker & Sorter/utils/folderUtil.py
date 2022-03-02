import os, shutil
from datetime import datetime;

SOURCE_FOLDER = "./temp";
TARGET_FOLDER = "./RESULT";
BACKUP_FOLDER = "./STAGING";

def printAction(action, fileNames):
    print("\n" + action  + " " + str(len(fileNames)) + " files");
    
def countFiles(pathToFolder):
    fileNames = os.listdir(pathToFolder);
    return len(fileNames);
    
def getFileNameOnly(filePath):
    splitted = filePath.split("/");
    return splitted[len(splitted)-1];

def deleteAllFiles(pathToFolder):
    fileNames = os.listdir(pathToFolder);
    printAction("Deleting", fileNames);
    for filename in fileNames:
        file_path = os.path.join(pathToFolder, filename);
        deleteFile(file_path);

def deleteFile(filePath):
    try:
        if os.path.isfile(filePath) or os.path.islink(filePath):
            os.unlink(filePath);
        elif os.path.isdir(filePath):
            shutil.rmtree(filePath)
    except Exception as e:
        raise Exception('Failed to delete %s. Reason: %s' % (filePath, e));
        
def moveAllFiles(srcFolder, dstFolder):
    fileNames = os.listdir(srcFolder);
    printAction("Moving", fileNames);
    for filename in fileNames:
        src = os.path.join(srcFolder, filename);
        dst = os.path.join(dstFolder, filename);
        moveFile(src, dst);

def moveFile(srcFilePath, dstFilePath):
    try:
        shutil.move(srcFilePath, dstFilePath);
    except Exception as e:
        raise Exception('Failed to move from %s to %s. Reason %s' % (srcFilePath, dstFilePath, e));

def copyAllFiles(srcFolder, dstFolder):
    fileNames = os.listdir(srcFolder);
    printAction("Copying", fileNames);
    for filename in fileNames:
        src = os.path.join(srcFolder, filename);
        dst = os.path.join(dstFolder, filename);
        copyFile(src, dst);
        
def copyFile(srcFilePath, dstFilePath):
    try:
        shutil.copyfile(srcFilePath, dstFilePath);
    except Exception as e:  
        raise Exception('Failed to copy from %s to %s. Reason %s' % (srcFilePath, dstFilePath, e));
        
def clearTempFolder(gui):
    gui.consoleInsert("Cleaning Temp Folder");
    try:
        deleteAllFiles(SOURCE_FOLDER);
        gui.consoleInsert("Temp Folder Cleaned");
    except Exception as e:
        gui.consoleInsert(str(e), "red");
        raise e;

def clearResultFolder(gui):
    gui.consoleInsert("Cleaning Result Folder");
    try:
        deleteAllFiles(TARGET_FOLDER);
        gui.consoleInsert("Result Folder Cleaned");
    except Exception as e:
        gui.consoleInsert(str(e), "red");
        raise e;
        
def clearStagingFolder(gui):
    gui.consoleInsert("Cleaning Staging Folder");
    try:
        deleteAllFiles(BACKUP_FOLDER);
        gui.consoleInsert("Staging Folder Cleaned");
    except Exception as e:
        gui.consoleInsert(str(e), "red");
        raise e;
        
def backupFiles(gui, filenames=[]):
    gui.consoleInsert("Backing up files...");
    fname = [];
    if(len(filenames)<1):
        fname=gui.filenames;
    else:
        fname=filenames;
    
    for f in fname:
        fileNameOnly = getFileNameOnly(f);
        gui.consoleInsert("Backing up " + f + " to " + SOURCE_FOLDER);
        try:
            copyFile(f, SOURCE_FOLDER+"/"+fileNameOnly);
        except Exception as e:
            gui.consoleInsert(str(e), "red");
            raise e;
    gui.consoleInsert("Finish backup files");
    
def stagingResult(gui=None):
    if(gui!=None):
        gui.consoleInsert("Staging result", "blue");
    stagingFolder = os.path.join(BACKUP_FOLDER, str(datetime.today().strftime('%d-%m-%Y_%H%M%S')), "stage result");
    if not os.path.exists(os.path.dirname(stagingFolder)):
        os.makedirs(stagingFolder);
    copyAllFiles(TARGET_FOLDER, stagingFolder);