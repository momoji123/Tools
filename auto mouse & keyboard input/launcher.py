import pyautogui
from Util.TaskBuilder import TaskBuilder, TaskMode
from Util.MouseTask import MouseBtn, TaskTyp
from Util.KeyboardTask import TaskType
import Util.TaskFactory as tf
from Util.TaskManager import TaskManager


def main():
    pyautogui.FAILSAFE = False
    tm = TaskManager()
    nameList = getNameList()
    classList = getClassList()
    print(nameList)
    print(classList)

    ### START JOB ###

    #open browser
    tm.addTask(tf.doLeftSingleClick(768, 1053))
    start(tm)

    #open explorer
    tm.addTask(tf.doLeftSingleClick(647, 1062))
    tm.addTask(tf.doLeftSingleClick(506, 942))
    start(tm)

    for i in range(len(nameList)):
        #move mouse to first foto
        tm.addTask(tf.doMoveMouse(291, 387))
        #drag to upload
        tm.addTask(tf.doDragMouse(912, 561))
        # wait until upload finish
        tm.addTask(tf.doWait(3))
        #click foto
        tm.addTask((tf.doLeftSingleClick(744, 569)))
        #move mouse to photo in canvas
        tm.addTask(tf.doMoveMouse(1498,561))
        #drag to frame
        tm.addTask(tf.doDragMouse(1402, 560))
        #click name
        tm.addTask(tf.doLeftDoubleClick(1652, 601))
        tm.addTask(tf.doKeyboardCombination(["ctrl", "a"]))
        #type name
        tm.addTask(tf.doKeyboardTyping(nameList[i]))
        tm.addTask(tf.doKeyboardPress(["enter"]))
        #type class
        tm.addTask(tf.doKeyboardTyping(classList[i]))

        #TODO: save
        #click share btn
        tm.addTask(tf.doLeftSingleClick(1857, 171))
        #click download btn
        tm.addTask(tf.doLeftSingleClick(1618, 785))
        # wait
        tm.addTask(tf.doWait(3))
        #download
        tm.addTask(tf.doLeftSingleClick(1679, 686))
        #wait
        tm.addTask(tf.doWait(9))

        #click option
        tm.addTask(tf.doLeftSingleClick(790, 505))
        tm.addTask(tf.doWait(0.5))
        #click delete
        tm.addTask(tf.doLeftSingleClick(941, 810))
        tm.addTask(tf.doWait(0.4))

        #click frame
        tm.addTask(tf.doLeftSingleClick(1402, 560))
        #delete
        tm.addTask(tf.doKeyboardPress(["delete"]))

        # move mouse to first foto in explorer
        tm.addTask(tf.doLeftSingleClick(291, 387))
        #delete photo in explorer
        tm.addTask(tf.doKeyboardCombination(["shift", "delete"]))
        tm.addTask(tf.doWait(0.3))
        tm.addTask(tf.doKeyboardPress(["enter"]))
        tm.addTask(tf.doWait(0.3))

    start(tm)


    #restart position
    #tm.addTask(tf.doLeftSingleClick(660,592))
    #

    #start(tm)
    ### END OF JOB ###



def start(tm:TaskManager):
    tm.startAllTasks()
    tm.setTasks([])


# helper method for particular job
def getNameList():
    file = openFile()
    lines = file.readlines()
    result = []
    for l in lines:
        splitted = l.split(",")
        result.append(splitted[0].replace("\n", ""))
    file.close()
    return result


def getClassList():
    file = openFile()
    lines = file.readlines();
    result = []
    for l in lines:
        splitted = l.split(",")
        result.append(splitted[1].replace("\n", ""))
    file.close()
    return result


def openFile():
    return open("XII MIPA 5 DATA NAMA.csv", "r")


if __name__=="__main__":
    main()
