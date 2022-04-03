import tkinter as tk
from components import Home


class GUIRoot:
    root = None
    home = None

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("SimpleEnc")
        background = tk.Canvas(self.root, width=1000, height=800)
        background.pack()
        self.runHome()
        self.root.mainloop()

    def runHome(self):
        if self.home is None:
            self.home = Home.run(self.root)


def start():
    GUIRoot()
