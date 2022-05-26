from Util.TaskBuilder import TaskBuilder, TaskMode
from Util.MouseTask import MouseBtn, TaskTyp
from Util.KeyboardTask import TaskType


def doClick(x, y, mouseBtn:MouseBtn, taskTyp:TaskTyp):
    task = TaskBuilder().build(TaskMode.MOUSE_TASK)
    task.setTaskTyp(taskTyp)
    task.setMouseBtn(mouseBtn)
    task.setPosition(x, y)
    return task


def doLeftSingleClick(x, y):
    return doClick(x, y, MouseBtn.LEFT, TaskTyp.SINGLE_CLICK)


def doLeftDoubleClick(x, y):
    return doClick(x, y, MouseBtn.LEFT, TaskTyp.DOUBLE_CLICK)

def doDragMouse(x, y, button:MouseBtn=MouseBtn.LEFT):
    dragTask = TaskBuilder().build(TaskMode.MOUSE_TASK)
    dragTask.setTaskTyp(TaskTyp.DRAG)
    dragTask.setPosition(x, y)
    dragTask.setMouseBtn(MouseBtn.LEFT)
    return dragTask

def doMoveMouse(x, y):
    moveTask = TaskBuilder().build(TaskMode.MOUSE_TASK)
    moveTask.setTaskTyp(TaskTyp.MOVE)
    moveTask.setPosition(x, y)
    return moveTask


def doKeyboardTyping(text):
    task = TaskBuilder().build(TaskMode.KEYBOARD_TASK)
    task.setTaskTyp(TaskType.TYPING)
    task.setText(text)
    return task


def doKeyboardPress(btns:[str]):
    task = TaskBuilder().build(TaskMode.KEYBOARD_TASK)
    task.setTaskTyp(TaskType.PRESS)
    task.setPressBtns(btns)
    return task


def doWait(duration:float):
    task = TaskBuilder().build(TaskMode.WAIT)
    task.setDuration(duration)
    return task


def doKeyboardCombination(btns:[str]):
    task = TaskBuilder().build(TaskMode.KEYBOARD_TASK)
    task.setTaskTyp(TaskType.COMBINATION)
    task.setPressBtns(btns)
    return task
