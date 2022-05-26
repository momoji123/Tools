import os

SOURCE_FOLDER = "PUT IMAGES HERE"
RESULT_FOLDER = "RESULT"

def getFileList(folderPath):
    filenames = os.listdir(folderPath)
    return filenames

def extractFilename(filenameWithExt):
    splitted = filenameWithExt.split("/")
    splitted = splitted[len(splitted)-1].split(".")
    result = "";
    for i in range(0,len(splitted)-1):
        result += splitted[i]
    return  result;

def extractExtension(filenameWithExt):
    splitted = filenameWithExt.split("/")
    splitted = splitted[len(splitted) - 1].split(".")
    return "."+splitted[len(splitted)-1]