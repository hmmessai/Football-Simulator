import tkinter as tk
import sys
import json
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

        title = tk.Label(self.content, text="Team Registration", font=('Arial', 20))
        title.grid(row=0, column=0, columnspan=5)

        label = tk.Label(self.content, text="Please enter the required information to register your team of desire. This step will register your team into our database for you to play oour simulation.")
        label.grid(row=1, column=0, columnspan=5, pady=10, padx=10)
        label.config(wraplength=600)

        name_label = tk.Label(self.content, text="Name of team")
        name_label.grid(row=2, column=0, pady=10, padx=10)
        self.name = tk.Entry(self.content, width=40)
        self.name.grid(row=2, column=1, sticky='w')
        self.name_error = tk.Label(self.content)
        self.name_error.grid(row=2, column=2, sticky='w')

        abbr_label = tk.Label(self.content, text="Abbreviated Name")
        abbr_label.grid(row=3, column=0, pady=10, padx=10)
        self.abbrv_name = tk.Entry(self.content)
        self.abbrv_name.grid(row=3, column=1, sticky='w')
        self.abv_error = tk.Label(self.content)
        self.abv_error.grid(row=3, column=2, sticky='w')

        year_label = tk.Label(self.content, text="Year founded")
        year_label.grid(row=4, column=0, pady=10, padx=10)
        self.year = tk.Entry(self.content)
        self.year.grid(row=4, column=1, sticky='w')
        self.year_error = tk.Label(self.content)
        self.year_error.grid(row=4, column=2, sticky='w')

        colors_label = tk.Label(self.content, text="Colors")
        colors_label.grid(row=5, column=0, pady=10, padx=10)
        self.colors = tk.Entry(self.content)
        self.colors.grid(row=5, column=1, sticky='w')
        self.colors_error = tk.Label(self.content)
        self.colors_error.grid(row=5, column=2, sticky='w')
        
        add_team_btn = tk.Button(self.content, text="Add Team", 
                           command=self.add_team)
        add_team_btn.grid(row=8, column=0, padx=10, pady=10)
        browse_team_btn = tk.Button(self.content, text="Browse Existing Teams", 
                           command=self.show_existing_teams)
        browse_team_btn.grid(row=8, column=1, padx=10, pady=10)

        navigate_btn = tk.Button(self.content, text="go to frame 1", 
                           command=lambda: controller.show_frame("FrameOne"))
        navigate_btn.grid(row=8, column=2, padx=10, pady=10)

        self.teams_container = tk.Listbox(self.content, width=30)
        self.teams_container.grid(row=9, column=0, columnspan=2, padx=10, pady=10, sticky='w')

        self.team_info = tk.Listbox(self.content, width=40)
        self.team_info.grid(row=9, column=1, columnspan=2, sticky='e')
        self.team_info.config(background="black")

        self.teams_container.bind("<<ListboxSelect>>", self.on_select_list)
        self.team_info.bind("<<ListboxSelect>>", None)

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
        # if selected_index and self.teams_container.get(selected_index[0]) not in self.selected_teams.get(0, tk.END):
        #     self.selected_teams.insert(tk.END, self.teams_container.get(selected_index))
        self.team_info.config(state="normal")
        self.team_info.delete(0, tk.END)
        for i in TeamInfo.teams:
            if str(i) == self.teams_container.get(selected_index):
                self.team_info.insert(tk.END, f"Name: {i.name}")
                self.team_info.insert(tk.END, f"Abbreviated Name: {i.abv_name}")
                self.team_info.insert(tk.END, f"Year founded: {i.year}")
                self.team_info.insert(tk.END, f"Colors: {i.colors}")
        self.team_info.config(state="disabled")
    
    def add_team(self):
        inputs = [self.name, self.abbrv_name, self.year, self.colors]
        errors = [self.name_error, self.abv_error, self.year_error, self.colors_error]
        
        for i, inputerror in enumerate(inputs):
            for x in errors:
                x.config(text="")
            if inputerror.get() == "":
                errors[i].config(text="This field cannot be left blank")
                return

        new_team = Team(name=self.name.get(), abv_name=self.abbrv_name.get(), year=self.year.get(), colors=self.colors.get())
        for i in TeamInfo.teams:
            if i is new_team:
                return
        TeamInfo.teams.append(new_team)
        with open('storage.json', 'w') as f:
            objs = {}
            for i in TeamInfo.teams:
                objs[i.name] = i.__dict__
            json.dump(objs, f)