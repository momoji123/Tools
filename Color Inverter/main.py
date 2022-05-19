from Util import DataManager, ImageEditor

try:
    filenames = DataManager.getFileList(DataManager.SOURCE_FOLDER)
except Exception as e:
    print(e)

try:
    print("Start converting " + str(len(filenames)) + " images...")
    counter = 0
    for filename in filenames:
        editor = ImageEditor.Editor(DataManager.SOURCE_FOLDER + "/" + filename)
        editor.invertColor()
        counter += 1
        if(counter%10 == 0):
            print(str(counter) + " Images complete. " + str(len(filenames) - counter) + " more")

    print(str(len(filenames)) + " images have been inverted")
except Exception as e:
    print(e)

input("press enter to exit")