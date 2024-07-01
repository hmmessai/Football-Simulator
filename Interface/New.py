import sys
import json
import tkinter as tk
import tkinter.font as tkFont
sys.path.append("")
sys.path.append("..")
from NewT import FrameOne
from NewT import TeamInfo
from NewT import Welcome

from classes import Team
from classes import Competition


class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("900x700")
        self.title("Football Simulator")

        # self.wm_attributes("-maxsize", self.winfo_width(), self.winfo_height())
        self.resizable(False, False)

        custom_bg = "grey"

        #Page Title
        self.page_title = tk.Frame(self, bg=custom_bg)
        self.page_title.pack(fill=tk.X, padx=5, pady=5)
        self.page_title.pack_propagate(flag=False)
        self.page_title.config(height=30)

        self.bold_font = tkFont.Font(family="Helvetica", size=12, weight="bold")
        self.normal_font = tkFont.Font(family="Helvetica", size=12, weight='normal')
        self.title_font = tkFont.Font(family="Helvetica", size=18, weight="bold")

        label = tk.Label(self.page_title, text="Football Simulator", font=self.bold_font, foreground="white", bg=custom_bg)
        label.pack(padx=5, pady=5)


        #Container
        self.container = tk.Frame(self)
        self.container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.container.pack_propagate(flag=False)


        #Dashboard
        self.dashboard = tk.Frame(self.container, bg=custom_bg)
        self.dashboard.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        self.dashboard.pack_propagate(flag=False)
        self.dashboard.config(width=230)

        welcome_button = tk.Button(self.dashboard, text="Welcome Page", font=self.normal_font, bg='black', borderwidth=0, highlightthickness=0, foreground='white', command=lambda: self.go_to("Welcome", welcome_button))
        welcome_button.place(relx=0, rely=0.1, relwidth=0.95, height=25)

        frameone_button = tk.Button(self.dashboard, text="Competitions Management", font=self.normal_font, bg='black', borderwidth=0, highlightthickness=0, foreground='white', command=lambda: self.go_to("FrameOne", frameone_button))
        frameone_button.place(relx=0, rely=0.17, relwidth=0.95, height=25)

        teaminfo_button = tk.Button(self.dashboard, text="Teams Management", font=self.normal_font, bg='black', borderwidth=0, highlightthickness=0, foreground='white', command=lambda: self.go_to("TeamInfo", teaminfo_button))
        teaminfo_button.place(relx=0, rely=0.24, relwidth=0.95, height=25)

        self.buttons = {
            "Welcome": welcome_button,
            "FrameOne": frameone_button,
            "TeamInfo": teaminfo_button
        }

        #Content
        self.content = tk.Frame(self.container)
        self.content.pack(fill=tk.BOTH, expand=True)
        self.content.pack_propagate(False)

        # Initialize frames dictionary
        self.frames = {}
        
        # Create frames
        self.create_frames()
        self.load_storage()
        
        # Show initial frame
        self.show_frame("FrameOne")
    
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
            frame.place(relwidth=1, relheight=1)
    
    def show_frame(self, frame_name):
        # Bring the frame to the front
        frame = self.frames[frame_name]
        for key, button in self.buttons.items():
            if key != frame_name:
                button.config(bg='black', foreground="white")
            else:
                button.config(bg='white', foreground="black")
        frame.tkraise()

    def go_to(self, name, reference):
        for key, button in self.buttons.items():
            if key != name:
                button.config(bg='black', foreground="white")
        reference.config(bg='white', foreground="black")
        self.show_frame(name)

    def load_storage(self):
        teams = {}
        competition = {}

        try:
            with open('storage.json', 'r+', encoding='utf-8') as f:
                content = f.read().strip()
                if content:
                    data = json.loads(content)
                    for k, v in data.items():
                        if k.split('.')[0] == 'Team':
                            teams[k] = Team(**v)
                        elif k.split('.')[1] == 'Competition':
                            competition[k] = Competition(**v)
                    print("Loaded teams from JSON:", teams)  # Debug statement

            for team in teams.values():
                if team not in TeamInfo.teams:
                    TeamInfo.teams.append(team)
                    print("Added team to TeamInfo.teams:", team)  # Debug statement

            print("Final TeamInfo.teams:", TeamInfo.teams)  # Debug statement
        except Exception as e:
            print(f"Error loading storage: {e}")

if __name__ == '__main__':
    app = MainApp()
    app.mainloop()