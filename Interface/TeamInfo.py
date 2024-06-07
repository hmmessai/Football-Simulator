import tkinter as tk
import sys
sys.path.append('..')
from classes import Team

class TeamInfo(tk.Frame):
    teams = []
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        ##Title##
        title = tk.Label(self, text="Team Information", font=('Arial', 20))
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

        label = tk.Label(self.content, text="This is Team Info")
        label.grid(row=0, column=0, pady=10, padx=10)

        name_label = tk.Label(self.content, text="Name of team")
        name_label.grid(row=1, column=0, pady=10, padx=10)
        self.name = tk.Entry(self.content)
        self.name.grid(row=1, column=1)
        
        add_team_btn = tk.Button(self.content, text="Add Team", 
                           command=self.add_team)
        add_team_btn.grid(row=2, column=0, padx=10, pady=10)
        browse_team_btn = tk.Button(self.content, text="Browse Existing Teams", 
                           command=self.show_existing_teams)
        browse_team_btn.grid(row=2, column=1, padx=10, pady=10)

        self.teams_container = tk.Listbox(self.content)
        self.teams_container.grid(row=3, column=0)

        self.selected_teams = tk.Listbox(self.content)
        self.selected_teams.grid(row=3, column=1)

        self.teams_container.bind("<<ListboxSelect>>", self.on_select_list)

        self.controller.bind("<Configure>", self.update_dashboard_width)

    def update_dashboard_width(self, event):
        # Update the width of self.dashboard when the window is resized
        self.dashboard.config(width=self.controller.winfo_width() // 3)
        self.dashboard.config(height=self.controller.winfo_height() - 50)

    def show_existing_teams(self):
        self.teams_container.delete(0, tk.END)
        for item in TeamInfo.teams:
            if item not in self.teams_container.get(0, tk.END):
                self.teams_container.insert(tk.END, item)

    def on_select_list(self, event):
        selected_index = self.teams_container.curselection()
        if selected_index and self.teams_container.get(selected_index[0]) not in self.selected_teams.get(0, tk.END):
            self.selected_teams.insert(tk.END, self.teams_container.get(selected_index))
    
    def add_team(self):
        new_team = Team(name=self.name.get())
        for i in TeamInfo.teams:
            if i is new_team:
                return
        print(new_team)
        TeamInfo.teams.append(new_team)