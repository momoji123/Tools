import pyautogui
from time import sleep

class TaskTyp:
    DOUBLE_CLICK="double"
    SINGLE_CLICK="single"
    DRAG="drag"
    MOVE="move"

class MouseBtn:
    RIGHT="right"
    LEFT="left"
    MIDDLE="middle"

class MouseTask:

    position=None
    mouseBtn:MouseBtn=None
    taskTyp:TaskTyp=None

    def __init__(self):
        self.position = pyautogui.position()
        self.mouseBtn = MouseBtn.LEFT
        self.taskTyp = TaskTyp.SINGLE_CLICK

    def setPosition(self, x, y):
        self.position = [x, y]
        return self

    def setMouseBtn(self, btn):
        self.mouseBtn = btn
        return self

    def setTaskTyp(self, clickTyp:TaskTyp):
        self.taskTyp = clickTyp
        return self

    def start(self):
        if self.position is None:
            return self
        if self.taskTyp is TaskTyp.SINGLE_CLICK:
            self.singleClick()
        elif self.taskTyp is TaskTyp.DOUBLE_CLICK:
            self.doubleClick()
        elif self.taskTyp is TaskTyp.MOVE:
            self.move()
        elif self.taskTyp is TaskTyp.DRAG:
            self.drag()
        return self

    def singleClick(self):
        self.move()
        pyautogui.click(pyautogui.position().x, pyautogui.position().y, button=self.mouseBtn)

    def doubleClick(self):
        self.move()
        pyautogui.doubleClick(pyautogui.position().x, pyautogui.position().y, button=self.mouseBtn)

    def drag(self):
        pyautogui.dragTo(self.position[0], self.position[1], duration=0.5, button=self.mouseBtn)

    def move(self):
        pyautogui.moveTo(self.position[0], self.position[1]);
