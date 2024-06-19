import tkinter as tk
import tkinter.font as tkFont

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("600x600")
        self.title("Dashboard")

        custom_bg = "grey"

        #Page Title
        self.page_title = tk.Frame(self, bg=custom_bg)
        self.page_title.pack(fill=tk.X, padx=5, pady=5)
        self.page_title.pack_propagate(flag=False)
        self.page_title.config(height=30)

        bold_font = tkFont.Font(family="Helvetica", size=12, weight="bold")

        label = tk.Label(self.page_title, text="Page Title", font=bold_font, foreground="white", bg=custom_bg)
        label.pack(padx=5, pady=5)


        #Container
        self.container = tk.Frame(self)
        self.container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.container.pack_propagate(flag=False)


        #Dashboard
        self.dashboard = tk.Frame(self.container, bg=custom_bg)
        self.dashboard.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        self.dashboard.pack_propagate(flag=False)
        self.dashboard.config(width=150)

        self.content = tk.Frame(self.container, bg='red')
        self.content.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.content.pack_propagate(flag=False)

if __name__ == '__main__':
    app = MainApp()
    app.mainloop()