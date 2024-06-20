import tkinter as tk

class FrameOne(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        label = tk.Label(self, text="This is Frame One")
        label.pack(padx=10, pady=10)

class TeamInfo(tk.Frame):
    teams = []

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        

class Welcome(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        label = tk.Label(self, text="Welcome!")
        label.pack(padx=10, pady=10)