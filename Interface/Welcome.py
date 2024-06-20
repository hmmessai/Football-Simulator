import tkinter as tk

class Welcome(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        label = tk.Label(self, text="Welcome to Football Simulator", font=('Arial', 20), foreground="blue")
        label.grid(column=0, row=0, pady=10, padx=10, sticky='nswe')

        self.content = tk.Label(self, text="This is a rough simulation of the game we all love and cherish. To get started, Add a competition name and procced to the next steps.", font=('Arial', 18))
        self.content.grid(row=1, column=0, pady=10, padx=10, sticky='nsew')

        button = tk.Button(self, text="Go to Frame One", 
                           command=lambda: controller.show_frame("FrameOne"))
        button.grid(column=0, row=2, padx=10, pady=10, sticky='nsew')

        self.controller.bind("<Configure>", self.update_dashboard_width)

    def update_dashboard_width(self, event):
       self.content.config(wraplength=self.controller.winfo_width() - 40)