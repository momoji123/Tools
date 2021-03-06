import pyautogui
import keyboard


class TaskType:
    TYPING="type"
    COMBINATION="combi"
    PRESS="press"


class KeyboardTask:

    taskTyp=None
    text=""
    pressBtn=[]

    def __init__(self):
        self.taskTyp = TaskType.TYPING

    def setTaskTyp(self, taskType:TaskType):
        self.taskTyp = taskType
        return self

    def setText(self, text):
        self.text = text
        return self

    def addPressBtn(self, btn:str):
        self.pressBtn.append(btn)
        return self

    def setPressBtns(self, btnSeries:[str]):
        self.pressBtn = btnSeries
        return self

    def start(self):
        try:
            if self.taskTyp is TaskType.TYPING:
                keyboard.write(self.text, 0.01)
            elif self.taskTyp is TaskType.PRESS:
                for btn in self.pressBtn:
                    keyboard.press(btn)
                    keyboard.release(btn)
            elif self.taskTyp is TaskType.COMBINATION:
                for i in range(len(self.pressBtn)):
                    btn = self.pressBtn[i]
                    if i == len(self.pressBtn)-1:
                        keyboard.press(btn)
                    else:
                        keyboard.press(btn)
        finally:
            for btn in self.pressBtn:
                keyboard.release(btn)
            self.pressBtn = []