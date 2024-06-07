import tkinter as tk

class FrameOne(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        ##Title##
        title = tk.Label(self, text="Frame one", font=('Arial', 20))
        title.grid(row=0, column=0)

        ##Dashboard##
        self.dashboard = tk.Frame(self, bd=2, relief="groove", highlightbackground="black")
        self.dashboard.grid(row=1, column=0, sticky='nsew')
        self.dashboard.grid_propagate(False)

        label1 = tk.Label(self.dashboard, text="Label1")
        label1.grid(row=0, column=0, sticky='nsew')

        label2 = tk.Label(self.dashboard, text="Label2")
        label2.grid(row=1, column=0, sticky='nsew')

        label3 = tk.Label(self.dashboard, text="Label3")
        label3.grid(row=2, column=0, sticky='nsew')

        label4 = tk.Label(self.dashboard, text="Label4")
        label4.grid(row=3, column=0, sticky='nsew')

        ##Content##
        self.content = tk.Frame(self)
        self.content.grid(row=1, column=1, sticky="nw")
        label = tk.Label(self.content, text="This is Frame One")
        label.grid(row=0, column=0, pady=10, padx=10)
        
        button = tk.Button(self.content, text="Go to Frame 1", 
                           command=lambda: controller.show_frame("Welcome"))
        button.grid(row=1, column=0)

        button = tk.Button(self.content, text="Go to Team Info", 
                           command=lambda: controller.show_frame("TeamInfo"))
        button.grid(row=1, column=1)

        self.controller.bind("<Configure>", self.update_dashboard_width)

    def update_dashboard_width(self, event):
        # Update the width of self.dashboard when the window is resized
        self.dashboard.config(width=self.controller.winfo_width() / 3)
        self.dashboard.config(height=self.controller.winfo_height() - 50)