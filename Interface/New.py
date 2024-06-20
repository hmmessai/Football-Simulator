import sys
import tkinter as tk
import tkinter.font as tkFont
sys.path.append("")
sys.path.append("..")
from NewT import FrameOne
from NewT import TeamInfo
from NewT import Welcome


class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("800x600")
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


        #Content
        self.content = tk.Frame(self.container, bg='red')
        self.content.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.content.pack_propagate(False)

        # Initialize frames dictionary
        self.frames = {}
        
        # Create frames
        self.create_frames()
        
        # Show initial frame
        self.show_frame("TeamInfo")
    
    def create_frames(self):
        # Create instances of frames and store them in the frames dictionary
        frame_one = FrameOne(parent=self.content, controller=self)
        teaminfo = TeamInfo(parent=self.content, controller=self)
        welcome = Welcome(parent=self.content, controller=self)
        
        self.frames["TeamInfo"] = teaminfo
        self.frames["FrameOne"] = frame_one
        self.frames["Welcome"] = welcome
        
        # Place all frames in the container but on top of each other
        for frame in self.frames.values():
            frame.grid(row=0, column=0, sticky="nsew")
    
    def show_frame(self, frame_name):
        # Bring the frame to the front
        frame = self.frames[frame_name]
        frame.tkraise()

if __name__ == '__main__':
    app = MainApp()
    app.mainloop()