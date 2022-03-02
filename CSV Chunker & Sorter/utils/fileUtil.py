import os;

SOURCE_FOLDER = "./temp";
TARGET_FOLDER = "./RESULT";
BACKUP_FOLDER = "./STAGING";

def openFile(fileName, fromFolder=""):
    if(fromFolder==""):
        targetFile = fileName;
    else:   
        targetFile = fromFolder + "/" + os.path.basename(fileName);
    return open(targetFile, "r");
    
def getWriter(fileName):
    targetFile = TARGET_FOLDER + "/" + fileName;
    writer = open(targetFile, "a");
    return writer;
    
def getWriterWithHeader(fileName, header):
    writer = getWriter(fileName);
    writer.write(header);
    return writer;