import os, shutil;

SOURCE = "./PUT FILES HERE";
SOURCE_CSV = "./PUT CSV HERE";
RESULT = "./RESULT";

class Copier:
    fromList=[];
    toList=[];
    
    def __init__(self, delimiter, fileExtension, sourceCSV):
        sourceCSVPath = SOURCE_CSV + "/" + sourceCSV;
        with open(sourceCSVPath, mode='r') as f:
            for line in f:
                split = line.split(delimiter);
                self.fromList.append(SOURCE + "/" + split[0].rstrip("\n") + fileExtension);
                self.toList.append(RESULT + "/" + split[1].rstrip("\n") + fileExtension);
                
    def doCopy(self):
        print("from list size: ", str(len(self.fromList)-1));
        for i in range(1,len(self.fromList)):
            shutil.copyfile(self.fromList[i], self.toList[i]);

def main():
    delimiter = input("Delimiter: ");
    fileExtension = input("File Extention (Optional if already included in csv): ");
    csvName = input("CSV File name: ");
    copier = Copier(delimiter, fileExtension, csvName);
    copier.doCopy();
    
if __name__=="__main__":
    main();
    