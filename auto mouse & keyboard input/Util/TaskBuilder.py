from Util import MouseTask, KeyboardTask, WaitingTask


class TaskBuilder:

    def build(self, taskMode):
        if taskMode == TaskMode.MOUSE_TASK:
            return MouseTask.MouseTask()
        if taskMode == TaskMode.KEYBOARD_TASK:
            return KeyboardTask.KeyboardTask()
        if taskMode == TaskMode.WAIT:
            return WaitingTask.WaitingTask()


class TaskMode:
    MOUSE_TASK = "MOUSE"
    KEYBOARD_TASK = "KEYBOARD"
    WAIT = "WAIT"
