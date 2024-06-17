
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
# from screeninfo import get_monitors
import sys
import json

sys.path.append('')
sys.path.append('..')
from classes import Team
from FrameOne import FrameOne
from Welcome import Welcome
from TeamInfo import TeamInfo


#monnitor = get_monitors()[0]
screen_width = 600#monnitor.width
screen_height = 400#monnitor.height

window_width = 800
window_height = 600

x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2


import tkinter as tk
from tkinter import ttk

class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Football Simulation")
        self.geometry(f"{window_width}x{window_height}")
        self.config(background="#bd3102")
        
        # Create a container frame
        self.container = tk.Frame(self)
        self.container.pack(padx=20, pady=20, anchor='center', fill="both", expand=True)
        
        # Initialize frames dictionary
        self.frames = {}
        
        # Create frames
        self.create_frames()
        
        # Show initial frame
        self.load_storage()
        self.show_frame("Welcome")
    
    def create_frames(self):
        # Create instances of frames and store them in the frames dictionary
        frame_one = FrameOne(parent=self.container, controller=self)
        teaminfo = TeamInfo(parent=self.container, controller=self)
        welcome = Welcome(parent=self.container, controller=self)
        
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

        if frame_name == "FrameOne":
            frame.update_teams()

    def load_storage(self):
        teams = {}

        try:
            with open('storage.json', 'r+', encoding='utf-8') as f:
                content = f.read().strip()
                if content:
                    data = json.loads(content)
                    for k, v in data.items():
                        teams[k] = Team(**v)
                    print("Loaded teams from JSON:", teams)  # Debug statement

            for team in teams.values():
                if team not in TeamInfo.teams:
                    TeamInfo.teams.append(team)
                    print("Added team to TeamInfo.teams:", team)  # Debug statement

            print("Final TeamInfo.teams:", TeamInfo.teams)  # Debug statement
        except Exception as e:
            print(f"Error loading storage: {e}")


if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()

