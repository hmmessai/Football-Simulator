import sys
import json
import tkinter as tk
from TeamInfo import TeamInfo

sys.path.append('..')
from classes import Competition

class FrameOne(tk.Frame):
    competitions = []
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        ##Dashboard##
        self.dashboard = tk.Frame(self, bd=2, relief="groove", highlightbackground="black")
        self.dashboard.grid(row=0, column=0, sticky='nsew')
        self.dashboard.grid_propagate(False)

        label1 = tk.Label(self.dashboard, text="Label1")
        label1.grid(row=0, column=0, sticky='nw')

        label2 = tk.Label(self.dashboard, text="Label2")
        label2.grid(row=1, column=0, sticky='nsew')

        label3 = tk.Label(self.dashboard, text="Label3")
        label3.grid(row=2, column=0, sticky='nsew')

        label4 = tk.Label(self.dashboard, text="Label4")
        label4.grid(row=3, column=0, sticky='nsew')

        ##Content##
        self.content = tk.Frame(self)
        self.content.grid(row=0, column=1, sticky="nw")
        label = tk.Label(self.content, text="Competition Registration", font=('Arial', 22))
        label.grid(row=0, column=0, pady=10, padx=10)
        
        button = tk.Button(self.content, text="Go to Frame 1", 
                           command=lambda: controller.show_frame("Welcome"))
        button.grid(row=1, column=0)

        button = tk.Button(self.content, text="Go to Team Info", 
                           command=lambda: controller.show_frame("TeamInfo"))
        button.grid(row=1, column=1)

        name_label = tk.Label(self.content, text="Name of competition")
        name_label.grid(row=2, column=0, pady=10, padx=10)
        self.name = tk.Entry(self.content, width=40)
        self.name.grid(row=2, column=1, sticky='w')
        self.name_error = tk.Label(self.content)
        self.name_error.grid(row=2, column=2, sticky='w')


        year_label = tk.Label(self.content, text="Number of teams")
        year_label.grid(row=4, column=0, pady=10, padx=10)
        self.totalTeam = tk.Entry(self.content)
        self.totalTeam.grid(row=4, column=1, sticky='w')
        self.totalTeam_error = tk.Label(self.content)
        self.totalTeam_error.grid(row=4, column=2, sticky='w')

        instruction_label = tk.Label(self.content, text="Select the teams you want participating in your competition. To remove the team selected it again", font=('Arial', 12))
        instruction_label.grid(row=5, column=0, columnspan=3, padx=10, pady=10, sticky='nsew')

        all_teams_label = tk.Label(self.content, text="All Teams", font=('Arial', 15))
        all_teams_label.grid(row=8, column=0, padx=10, pady=10, columnspan=2, sticky='w')
        self.teams_container = tk.Listbox(self.content, width=30)
        self.teams_container.grid(row=9, column=0, padx=10, pady=10, sticky='w')
        self.update_teams()

        arrow_label = tk.Label(self.content, text="===>", font=('Arial', 10))
        arrow_label.grid(row=9, column=1, sticky='w')
        arrow_label.config(wraplength=600)

        selected_teams_label = tk.Label(self.content, text="Selected Teams", font=('Arial', 15))
        selected_teams_label.grid(row=8, column=2, padx=10, pady=10, columnspan=2, sticky='w')
        self.selected_teams = tk.Listbox(self.content, width=30)
        self.selected_teams.grid(row=9, column=2, sticky='w')
        self.selected_teams.config(background="black", foreground="white")

        self.competition_error = tk.Label(self.content, text="")
        self.competition_error.grid(row=10, column=0, sticky='nsew')
        self.competition_error.config(wraplength=200)

        add_team_btn = tk.Button(self.content, text="Create Competition", 
                           command=self.create_competition)
        add_team_btn.grid(row=10, column=1, sticky='w')
        

        self.teams_container.bind("<<ListboxSelect>>", self.on_select_list)
        self.controller.bind("<Configure>", self.update_dashboard_width)

    def create_competition(self):
        inputs = [self.name, self.totalTeam]
        errors = [self.name_error, self.totalTeam_error]
        
        for i, inputerror in enumerate(inputs):
            for x in errors:
                x.config(text="")
            if inputerror.get() == "":
                errors[i].config(text="This field cannot be left blank")
                return
            
        if len(self.selected_teams.get(0, tk.END)) == 0 or len(self.selected_teams.get(0, tk.END)) > int(self.totalTeam.get()):
            self.competition_error.config(text="The number of participant teams is not correct please adjust it according to the Total teams number you entered")

        teams = []
        for i in TeamInfo.teams:
            if str(i) in self.selected_teams.get(0, tk.END):
                teams.append(i)
        try:
            comp = Competition(self.name.get(), 'tournament', int(self.totalTeam.get()), teams)
            print(comp)
            print(comp.teams)
            FrameOne.competitions.append(comp)
        except Exception as e:
            self.competition_error.config(text=e)

        with open('storage.json', 'r') as f:
            objs = json.load(f)
        with open('storage.json', 'w') as f:
            for i in FrameOne.competitions:
                key = 'Competition.' + i.name
                inner_dict = {}
                for k, v in i.__dict__.items():
                    if k == 'teams':
                        inner_dict[k] = str(v)
                    else:
                        inner_dict[k] = v
                objs[key] = inner_dict

            json.dump(objs, f, indent=4)


    def update_teams(self):
        # Clear the listbox
        self.teams_container.delete(0, tk.END)

        # Insert new items
        for team in TeamInfo.teams:
            self.teams_container.insert(tk.END, team)

    def on_select_list(self, event):
        selected_index = self.teams_container.curselection()

        if selected_index:
            selected_item = self.teams_container.get(selected_index[0])
            
            # Check if the item is already in the selected_teams Listbox
            if selected_item not in self.selected_teams.get(0, tk.END):
                self.selected_teams.insert(tk.END, selected_item)
            else:
                # Remove the item from the selected_teams Listbox
                for i in range(self.selected_teams.size()):
                    if self.selected_teams.get(i) == selected_item:
                        self.selected_teams.delete(i)
                        break  # Exit the loop once the item is found and deleted
                

    def update_dashboard_width(self, event):
        # Update the width of self.dashboard when the window is resized
        self.dashboard.config(width=self.controller.winfo_width() / 3)
        self.dashboard.config(height=self.controller.winfo_height() - 50)