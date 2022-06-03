import pyautogui
from Util.TaskBuilder import TaskBuilder, TaskMode
from Util.MouseTask import MouseBtn, TaskTyp
from Util.KeyboardTask import TaskType
import Util.TaskFactory as tf
from Util.TaskManager import TaskManager
from ThreadJob.JobManager import JobManager
from ThreadJob.JobThread import JobThread
import keyboard
import sys


def main():
    pyautogui.FAILSAFE = False
    tm = TaskManager()
    jobManager = JobManager()

    ### START JOB ###
    nameList = getNameList()
    classList = getClassList()

    #openBrowser
    tm.addTask(tf.doLeftSingleClick(769, 1055))

    #open explorer
    tm.addTask(tf.doLeftSingleClick(650, 1054))
    tm.addTask(tf.doLeftSingleClick(511, 940))

    for i in range(len(nameList)):
        # reset point
        resetPoint(tm)

        #insert name
        tm.addTask(tf.doLeftDoubleClick(1474, 669))
        tm.addTask(tf.doKeyboardCombination(["ctrl", "a"]))
        tm.addTask(tf.doKeyboardTyping(nameList[i]))

        #reset point
        resetPoint(tm)

        #insert class
        tm.addTask(tf.doLeftDoubleClick(1474, 723))
        tm.addTask(tf.doKeyboardCombination(["ctrl", "a"]))
        tm.addTask(tf.doKeyboardTyping(classList[i]))

        # reset point
        resetPoint(tm)

        #move to photo
        tm.addTask(tf.doMoveMouse(344, 382))
        #drag
        tm.addTask(tf.doDragMouse(684, 521))
        tm.addTask(tf.doWait(2))
        #click photo to insert
        tm.addTask(tf.doLeftSingleClick(676, 568))

        # reset point
        resetPoint(tm)

        #move to photo
        tm.addTask(tf.doMoveMouse(1467, 529))
        #drag to frame
        tm.addTask(tf.doDragMouse(1547, 528))

        # reset point
        resetPoint(tm)

        #share
        tm.addTask(tf.doLeftSingleClick(1856, 166))
        #download btn
        tm.addTask(tf.doLeftSingleClick(1628, 765))
        #click dropdown
        tm.addTask(tf.doLeftSingleClick(1631, 347))
        #click type
        tm.addTask(tf.doLeftSingleClick(1562, 632))
        tm.addTask(tf.doWait(1.5))
        #donwload
        tm.addTask(tf.doLeftSingleClick(1652, 493))
        tm.addTask(tf.doWait(25))

        #click option
        tm.addTask(tf.doLeftSingleClick(711, 508))
        tm.addTask(tf.doWait(0.5))
        #delete
        tm.addTask(tf.doLeftSingleClick(871, 830))
        #click frame
        tm.addTask(tf.doLeftSingleClick(1475, 516))
        #delete
        tm.addTask(tf.doKeyboardPress(["delete"]))
        #click photo
        tm.addTask(tf.doLeftSingleClick(329, 368))
        tm.addTask(tf.doKeyboardCombination(["shift", "delete"]))
        tm.addTask(tf.doWait(0.5))
        tm.addTask(tf.doKeyboardPress(["enter"]))
        tm.addTask(tf.doWait(1))

    ### END OF JOB ###

    jobManager.registerTask(tm)
    runningThread = start(jobManager)
    while runningThread.is_alive():
        if keyboard.is_pressed("esc") is True and  keyboard.is_pressed("ctrl"):
            sys.exit(1)

def resetPoint(tm):
    tm.addTask(tf.doLeftSingleClick(1196, 303))

def registerTask(tm, jm:JobManager):
    jm.registerTask(tm)


def start(jobManager:JobManager):
    runningThread = JobThread(jobManager)
    runningThread.setDaemon(True)
    runningThread.start()
    return runningThread


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
    lines = file.readlines()
    result = []
    for l in lines:
        splitted = l.split(",")
        result.append(splitted[1].replace("\n", ""))
    file.close()
    return result


def openFile():
    return open("list mipa 3.csv", "r")


if __name__=="__main__":
    main()
