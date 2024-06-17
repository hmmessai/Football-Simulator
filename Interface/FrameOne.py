import tkinter as tk
from TeamInfo import TeamInfo

class FrameOne(tk.Frame):
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
                           command=None)


        all_teams_label = tk.Label(self.content, text="All Teams", font=('Arial', 15))
        all_teams_label.grid(row=8, column=0, padx=10, pady=10, columnspan=2, sticky='w')
        self.teams_container = tk.Listbox(self.content, width=30)
        self.teams_container.grid(row=9, column=0, columnspan=2, padx=10, pady=10, sticky='w')
        self.update_teams()

        selected_teams_label = tk.Label(self.content, text="Selected Teams", font=('Arial', 15))
        selected_teams_label.grid(row=8, column=1, padx=10, pady=10, columnspan=2, sticky='w')
        self.selected_teams = tk.Listbox(self.content, width=30)
        self.selected_teams.grid(row=9, column=1, columnspan=2, sticky='e')
        self.selected_teams.config(background="black", foreground="white")

        self.teams_container.bind("<<ListboxSelect>>", self.on_select_list)
        self.controller.bind("<Configure>", self.update_dashboard_width)

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