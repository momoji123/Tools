from Util import DataManager, DOCBuilder

def main():
    image_paths = DataManager.getFileList(DataManager.SOURCE_FOLDER)
    filename = input("result filename (WITHOUT extension .docx) : ")
    width = input("image width (Inches): ")
    height = input("image height(Inches): ")
    columns = input("number of column: ")
    rows = input("number of rows: ")

    builder = DOCBuilder.builder(filename+".docx")
    for path in image_paths:
        builder.addImage(DataManager.SOURCE_FOLDER + "/" + path, float(width), float(height))
    builder.setLayout(int(columns), int(rows))
    builder.doWrap()

if __name__=="__main__":
    main()