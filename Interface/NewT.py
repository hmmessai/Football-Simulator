import json
import tkinter as tk
from classes import Competition

class FrameOne(tk.Frame):

    competitions = []

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        title = tk.Label(self, text='Competitions Management', font=self.controller.title_font, anchor='center', justify='center')
        title.pack(fill='x', padx=5, pady=30)


        # Frame for dynamic content
        self.content = tk.Frame(self)
        self.content.pack(fill='both', expand=True)

        # Grid configuration
        self.content.grid_columnconfigure(0, weight=1)

        self.main_select()


    def main_select(self):

        self.clear_frame()
        self.content.grid_columnconfigure(1, weight=0)
        self.content.grid_columnconfigure(2, weight=0)
        self.content.grid_columnconfigure(3, weight=0)
        # Buttons
        create_button = tk.Button(self.content, text="Create Competition", 
                                  font=self.controller.normal_font, 
                                  anchor='center', 
                                  justify='center', 
                                  bg='black', 
                                  foreground='white', 
                                  borderwidth=0, 
                                  command=self.create_competition)
        create_button.grid(row=0, column=0, padx=5, pady=10)

        browse_button = tk.Button(self.content, text="Show Existing Competitions", 
                                  font=self.controller.normal_font, 
                                  anchor='center', 
                                  justify='center', 
                                  bg='black', 
                                  foreground='white', 
                                  borderwidth=0, 
                                  command=self.view_all_competitions)
        browse_button.grid(row=1, column=0, padx=5, pady=10)


    def update_teams(self):
        self.teams_container.delete(0, tk.END)

        # Insert new items
        for team in TeamInfo.teams:
            self.teams_container.insert(tk.END, team)

    def create_competition(self):
        self.clear_frame()

        self.content.grid_columnconfigure(1, weight=1)
        self.name = tk.StringVar()
        self.country = tk.StringVar()
        self.team_capacity = tk.IntVar()

        back_button = tk.Button(self.content, text="Go Back", bg='black', foreground='white', command=self.main_select)
        back_button.grid(row=1, column=0, padx=40, pady=5, sticky='w')

        name_label = tk.Label(self.content, text="Name of Competition")
        name_label.grid(row=2, column=0, pady=5, padx=10, sticky='e')
        
        name_entry = tk.Entry(self.content, textvariable=self.name)
        name_entry.grid(row=2, column=1, sticky='w', padx=10, pady=5)

        self.name_error = tk.Label(self.content)
        self.name_error.grid(row=3, column=1)

        country_label = tk.Label(self.content, text="Country of origin")
        country_label.grid(row=4, column=0, pady=5, padx=10, sticky='e')

        country_entry = tk.Entry(self.content, textvariable=self.country)
        country_entry.grid(row=4, column=1, sticky='w', padx=10, pady=5)

        self.country_error = tk.Label(self.content)
        self.country_error.grid(row=5, column=1)

        teams_capacity_label = tk.Label(self.content, text="Teams capacity")
        teams_capacity_label.grid(row=6, column=0, pady=0, padx=10, sticky='e')

        teams_capacity_entry = tk.Entry(self.content, textvariable=self.team_capacity)
        teams_capacity_entry.grid(row=6, column=1, sticky='w', padx=10, pady=0)

        self.teams_capacity_error = tk.Label(self.content)
        self.teams_capacity_error.grid(row=7, column=1)

        teams_select_label = tk.Label(self.content, text="Available Teams")
        teams_select_label.grid(row=8, column=0, pady=10, padx=30, sticky='e')

        self.teams_select_listbox = tk.Listbox(self.content)
        self.teams_select_listbox.grid(row=9, column=0, padx=30, pady=5, sticky='e')
        self.teams_select_listbox.config(width=100)
        self.update_teams()

        teams_select_label = tk.Label(self.content, text="Selected Teams")
        teams_select_label.grid(row=8, column=1, pady=5, padx=30, sticky='w')

        self.teams_selected_listbox = tk.Listbox(self.content)
        self.teams_selected_listbox.grid(row=9, column=1, padx=30, pady=5, sticky='w')
        self.teams_selected_listbox.config(width=100)

        self.competition_error = tk.Label(self.content, foreground='red')
        self.competition_error.grid(row=10, column=0)

        done_button = tk.Button(self.content, text="Create Competition", bg='black', foreground='white', command=self.store_competition)
        done_button.grid(row=11, column=1, padx=40, pady=20, sticky='e')

        self.teams_select_listbox.bind("<<ListboxSelect>>", self.on_select_list)


    def view_all_competitions(self):
        self.clear_frame()

        show_buttons = [
            tk.Button(self.content, text="View", bg='#5b648f', foreground='white', borderwidth=0, padx=20),
            tk.Button(self.content, text="Edit", bg='#5b648f', foreground='white', borderwidth=0, padx=20),
            tk.Button(self.content, text="Delete", bg='#5b648f', foreground='white', borderwidth=0, padx=20)]
        
        def view_options(row, comp):
            self.content.grid_columnconfigure(1, weight=1)
            self.content.grid_columnconfigure(2, weight=1)
            self.content.grid_columnconfigure(3, weight=1)
            for i, but in enumerate(show_buttons):
                if but.cget("text") == 'View':
                    but.config(command=lambda c=comp: self.view_competition(c))
                elif but.cget("text") == 'Edit':
                    but.config(command=lambda c=comp: self.edit_competition(c))
                elif but.cget("text") == 'Delete':
                    but.config(command=lambda c=comp: self.delete_competition(c))
                but.grid(row=row - 1, column=i + 1, sticky='w', padx=0, pady=5)
                

        back_button = tk.Button(self.content, text="Go Back", bg='black', foreground='white', command=self.main_select)
        back_button.grid(row=1, column=0, padx=40, pady=5, sticky='w')

        self.content.grid_columnconfigure(1, weight=0)
        self.content.grid_columnconfigure(2, weight=0)
        self.content.grid_columnconfigure(3, weight=0)
        for i, comp in enumerate(FrameOne.competitions):
            button = tk.Button(self.content, padx=20, pady=5, 
                               bg='black',
                               foreground='white',
                               font=self.controller.normal_font,
                               text=comp.name,
                               borderwidth=0,
                               command=lambda i=i, comp=comp: view_options(i + 3, comp))
            button.grid(row=i+2, column=0, padx=5, pady=5)


    def delete_competition(self, comp):
        
        with open('storage.json', 'r') as f:
            objs = json.load(f)

        print(objs)
        key_to_delete = f"Competition.{comp.name}"
        del objs[key_to_delete]
        for competition in FrameOne.competitions:
            if competition.name == comp.name:
                FrameOne.competitions.remove(competition)

        with open('storage.json', 'w') as f:
            json.dump(objs, f, indent=4)

        self.controller.load_storage(edit=True)
        self.view_all_competitions()

    def edit_competition(self, comp):
        """Competition editing page"""
        self.clear_frame()

        self.content.grid_columnconfigure(1, weight=1)
        name_var = tk.StringVar()
        country_var = tk.StringVar()
        team_capacity_var = tk.IntVar()

        back_button = tk.Button(self.content, text="Go Back", bg='black', foreground='white', command=self.view_all_competitions)
        back_button.grid(row=1, column=0, padx=40, pady=5, sticky='w')

        name_label = tk.Label(self.content, text="Name of Competition")
        name_label.grid(row=2, column=0, pady=5, padx=10, sticky='e')
        
        name_entry = tk.Entry(self.content, textvariable=name_var)
        name_entry.insert(tk.END, comp.name)
        name_entry.grid(row=2, column=1, sticky='w', padx=10, pady=5)

        self.name_error = tk.Label(self.content)
        self.name_error.grid(row=3, column=1)

        country_label = tk.Label(self.content, text="Country of origin")
        country_label.grid(row=4, column=0, pady=5, padx=10, sticky='e')

        country_entry = tk.Entry(self.content, textvariable=country_var)
        country_entry.insert(tk.END, comp.country)
        country_entry.grid(row=4, column=1, sticky='w', padx=10, pady=5)

        self.country_error = tk.Label(self.content)
        self.country_error.grid(row=5, column=1)

        teams_capacity_label = tk.Label(self.content, text="Teams capacity")
        teams_capacity_label.grid(row=6, column=0, pady=0, padx=10, sticky='e')

        teams_capacity_entry = tk.Entry(self.content, textvariable=team_capacity_var)
        teams_capacity_entry.insert(tk.END, comp.totalTeams)
        teams_capacity_entry.grid(row=6, column=1, sticky='w', padx=10, pady=0)

        self.teams_capacity_error = tk.Label(self.content)
        self.teams_capacity_error.grid(row=7, column=1)

        teams_select_label = tk.Label(self.content, text="Available Teams")
        teams_select_label.grid(row=8, column=0, pady=10, padx=30, sticky='e')

        self.teams_select_listbox = tk.Listbox(self.content)
        self.teams_select_listbox.grid(row=9, column=0, padx=30, pady=5, sticky='e')
        self.teams_select_listbox.config(width=100)
        self.update_teams()

        teams_select_label = tk.Label(self.content, text="Selected Teams")
        teams_select_label.grid(row=8, column=1, pady=5, padx=30, sticky='w')

        self.teams_selected_listbox = tk.Listbox(self.content)
        for i in comp.teams:
            self.teams_selected_listbox.insert(tk.END, i)
        self.teams_selected_listbox.grid(row=9, column=1, padx=30, pady=5, sticky='w')
        self.teams_selected_listbox.config(width=100)

        self.competition_error = tk.Label(self.content, foreground='red')
        self.competition_error.grid(row=10, column=0)

        done_button = tk.Button(self.content, text="Edit Competition", bg='black', foreground='white', command=lambda comp=comp: edit(comp))
        done_button.grid(row=11, column=1, padx=40, pady=20, sticky='e')

        def edit(comp):
            teams = []
            original_name = comp.name

            inputs = [name_var, country_var, team_capacity_var]
            errors = [self.name_error, self.country_error, self.teams_capacity_error]

            for i, inputerror in enumerate(inputs):
                for x in errors:
                    x.config(text="")
                try:
                    if inputerror.get() == "" or inputerror.get() == 0:
                        if i == 2:
                            errors[i].config(text="This field cannot be zero", foreground='red')
                        else:
                            errors[i].config(text="This field cannot be left blank", foreground='red')
                        return
                except Exception as e:
                    errors[i].config(text="Unexpected value entered", foreground='red')
                    return
                
            if len(self.teams_selected_listbox.get(0, tk.END)) > int(team_capacity_var.get()):
                self.competition_error.config(text="The number of participant teams is not correct please adjust it according to the Total teams number you entered", wraplength=240)
                return

            if len(self.teams_selected_listbox.get(0, tk.END)) == 0:
                self.competition_error.config(text="You need to choose atleast one team from the given teams or create a team of your own by going to the teams management panel.", wraplength=240)            
                return

            for i in TeamInfo.teams:
                if str(i) in self.teams_selected_listbox.get(0, tk.END):
                    teams.append(i)
            try:
                comp.name = name_var.get()
                comp.country = country_var.get()
                comp.totalTeam = team_capacity_var.get()
                comp.teams = teams
            except ValueError as ve:
                self.competition_error.config(text=ve, wraplength=240)
                return
            except Exception as e:
                self.competition_error.config(text=e, wraplength=240)
                return

            with open('storage.json', 'r') as f:
                objs = json.load(f)

            comp_index = f"Competition.{original_name}"

            inner_dict = {
                'name': comp.name,
                'type': comp.type,
                'country': comp.country,
                'totalTeams': comp.totalTeam,
                'teams': [team.__dict__ for team in teams]
            }
            del objs[comp_index]

            new_index = f"Competition.{comp.name}"

            objs[new_index] = inner_dict

            try:
                with open('storage.json', 'w') as f:
                    json.dump(objs, f, indent=4)
            except Exception as e:
                self.competition_error.config(text=f"Error writing JSON file: {e}", wraplength=240)
                return

            self.controller.load_storage(edit=True)
            self.main_select()

        self.teams_select_listbox.bind("<<ListboxSelect>>", self.on_select_list)


    def view_competition(self, comp):
        """Competition viewing page"""
        self.clear_frame()

        back_button = tk.Button(self.content, text="Go Back", bg='black', foreground='white', command=self.view_all_competitions)
        back_button.grid(row=1, column=0, padx=40, pady=5, sticky='w')

        self.content.grid_columnconfigure(1, weight=0)
        self.content.grid_columnconfigure(2, weight=0)
        info_container = tk.Frame(self.content, bg='black')
        info_container.grid(row=2, column=0, padx=40, pady=10, sticky='nsew')
        name = tk.Label(info_container, text=f"Name:\t{comp.name}", font=self.controller.normal_font, bg='black', foreground='white')
        name.grid(row=2, column=0, padx=160, pady=5, sticky='w')
        country = tk.Label(info_container, text=f"Country:\t{comp.country}", font=self.controller.normal_font, bg='black', foreground='white')
        country.grid(row=3, column=0, padx=160, pady=5, sticky='w')

        capacity = tk.Label(info_container, text=f"Total number of teams participating: {comp.totalTeams}", font=self.controller.normal_font, bg='black', foreground='white')
        capacity.grid(row=4, column=0, padx=160, pady=5, sticky='w')

        capacity = tk.Label(info_container, text=f"Total number of teams registered: {comp.teamsCount}", font=self.controller.normal_font, bg='black', foreground='white')
        capacity.grid(row=5, column=0, padx=160, pady=5, sticky='w')

        teams = tk.Label(info_container, text=f"Teams:", font=self.controller.normal_font, bg='black', foreground='white')
        teams.grid(row=6, column=0, padx=160, pady=5, sticky='w')

        for index, team in enumerate(comp.teams):
            team_label = tk.Label(info_container, text=team.name, font=self.controller.normal_font, bg='black', foreground='white')
            team_label.grid(row=7+index, column=0, padx=40, pady=5, sticky='nsew')
        # canvas = tk.Canvas(self.content, width=50, height=50)
        # canvas.grid(row=4, column=0, padx=260, pady=5, sticky='e')

        # x, y, r = 25, 25, 20  
        # canvas.create_oval(x - r, y - r, x + r, y + r, fill='blue', outline='black')



    def store_competition(self):
        inputs = [self.name, self.country, self.team_capacity]
        errors = [self.name_error, self.country_error, self.teams_capacity_error]
        
        for i, inputerror in enumerate(inputs):
            for x in errors:
                x.config(text="")
            try:
                if inputerror.get() == "" or inputerror.get() == 0:
                    if i == 2:
                        errors[i].config(text="This field cannot be zero", foreground='red')
                    else:
                        errors[i].config(text="This field cannot be left blank", foreground='red')
                    return
            except Exception as e:
                errors[i].config(text="Unexpected value entered", foreground='red')
                return
            
        if len(self.teams_selected_listbox.get(0, tk.END)) > int(self.team_capacity.get()):
            self.competition_error.config(text="The number of participant teams is not correct please adjust it according to the Total teams number you entered", wraplength=240)
            return

        if len(self.teams_selected_listbox.get(0, tk.END)) == 0:
            self.competition_error.config(text="You need to choose atleast one team from the given teams or create a team of your own by going to the teams management panel.", wraplength=240)            
            return


        teams = []
        for i in TeamInfo.teams:
            if str(i) in self.teams_selected_listbox.get(0, tk.END):
                teams.append(i)
        try:
            comp = Competition(self.name.get(), 'league', int(self.team_capacity.get()), teams, country=self.country.get())
            print(comp)
            print(comp.teams)
            FrameOne.competitions.append(comp)
        except ValueError as ve:
            self.competition_error.config(text=ve, wraplength=240)
            return
        except Exception as e:
            self.competition_error.config(text=e, wraplength=240)
            return

        with open('storage.json', 'r') as f:
            objs = json.load(f)
        with open('storage.json', 'w') as f:
            for i in FrameOne.competitions:
                key = 'Competition.' + i.name
                inner_dict = {}
                for k, v in i.__dict__.items():
                    if k == 'teams':
                        teams = []
                        for i in v:
                            teams.append(i.__dict__)
                        inner_dict[k] = teams
                    else:
                        inner_dict[k] = v
                objs[key] = inner_dict

            json.dump(objs, f, indent=4)

            self.main_select()

    def update_teams(self):
        # Clear the listbox
        self.teams_select_listbox.delete(0, tk.END)

        # Insert new items
        for team in TeamInfo.teams:
            self.teams_select_listbox.insert(tk.END, team)

    def on_select_list(self, event):
        selected_index = self.teams_select_listbox.curselection()

        if selected_index:
            selected_item = self.teams_select_listbox.get(selected_index[0])
            
            # Check if the item is already in the selected_teams Listbox
            if selected_item not in self.teams_selected_listbox.get(0, tk.END):
                self.teams_selected_listbox.insert(tk.END, selected_item)
            else:
                # Remove the item from the teams_selected_listbox Listbox
                for i in range(self.teams_selected_listbox.size()):
                    if self.teams_selected_listbox.get(i) == selected_item:
                        self.teams_selected_listbox.delete(i)
                        break  # Exit the loop once the item is found and deleted
                

    def clear_frame(self):
        for widget in self.content.winfo_children():
            widget.destroy()

class TeamInfo(tk.Frame):
    teams = []

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        

class Welcome(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        label = tk.Label(self, text="Welcome to Football Simulator", font=self.controller.title_font)
        label.grid(row=0, column=0, padx=5, pady=30)

        self.content = tk.Label(self, text="This is a rough simulation of the game we all love and cherish. To get started, Add a competition name and procced to the next steps.", font=self.controller.normal_font)
        self.content.grid(row=1, column=0, padx=5, pady=5)

        button = tk.Button(self, text="Go to Frame One", 
                           command=lambda: controller.show_frame("FrameOne"))
        button.grid(row=2, column=0, padx=5, pady=5)

        self.controller.bind("<Configure>", self.update_dashboard_width)
    
    def update_dashboard_width(self, event):
       self.content.config(wraplength=self.controller.winfo_width() - 210)