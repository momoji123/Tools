from PyPDF2 import PdfFileMerger
import os;
import re;


sourceFolder = './PUT FILE HERE'
resultFolder = './RESULT'

filenames = os.listdir(sourceFolder);

keyContainer = [];

coverFile = input("cover file: ");
patternInput = input("pattern: ");
filePattern = re.compile(".*" + patternInput + ".*");

def extractKey(filename):
    split = filename.split(patternInput);
    return split[len(split)-1];

def addKey(file, defaultFile):
    print(file)
    key = extractKey(file);
    if key not in keyContainer:
        keyContainer.append(key);

def doMerge(fileContainer, resultFile):
    merger = PdfFileMerger()
    for pdf in fileContainer:
        merger.append(sourceFolder + "/" +pdf)
    merger.write(resultFolder + "/" + resultFile)
    merger.close()
    
def getExtension(filename):
    split = filename.split(".");
    ext = split[len(split)-1];
    return "."+ext;


for filename in filenames:
    if(getExtension(filename)==".pdf" and filePattern.match(filename)):
        addKey(filename, coverFile);

for i in range(len(keyContainer)):
    key = keyContainer[i];
    fileContainer = [];
    for filename in filenames:
        if (filename==coverFile or (getExtension(filename)==".pdf" and filePattern.match(filename) and key==extractKey(filename))):
            fileContainer.append(filename);
    print(fileContainer)
    doMerge(fileContainer, key);
    