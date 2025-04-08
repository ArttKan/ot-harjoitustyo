import tkinter as tk
from tkinter import messagebox
from services.score_service import ScoreService
from entities.team import Team
from entities.player import Player
from entities.game import Game


Scorekeeper = ScoreService()
current_game = None

EVENT_TYPES = ["2-Pointer", "3-Pointer", "Rebound", "Foul", "Technical Foul"]

team1 = Team("Golden State Warriors")
team2 = Team("Los Angeles Lakers")
team1.add_player(Player("Stephen Curry"))
team1.add_player(Player("Draymond Green"))
team2.add_player(Player("Luka Doncic"))
team2.add_player(Player("LeBron James"))
teams = [team1, team2]
selected_teams_label = "Choose teams"


def start_new_game():
    global current_game
    current_game = Game()  # Create a new game entity
    start_game_frame.grid_forget()  # Hide the start game frame
    # Show the team selection frame
    team1_selection_frame.grid(row=0, column=0, columnspan=2, pady=10)


def handle_add_event():
    event_type = selected_event_type.get()
    event_content = event_content_entry.get()

    if not event_type or not event_content:
        messagebox.showerror("Error", "Please fill in all fields.")
        return

    try:
        event_content = int(event_content)
    except ValueError:
        messagebox.showerror("Error", "Content must be a number.")
        return

    Scorekeeper.add_event(event_type, event_content)
    messagebox.showinfo("Success", f"Event '{event_type}' added successfully!")
    event_content_entry.delete(0, tk.END)

    update_event_list()


def update_event_list():
    event_listbox.delete(0, tk.END)
    events = Scorekeeper.get_events()
    for event in events:
        event_listbox.insert(tk.END, f"{event.type} - Score: {event.content}")


def handle_team1_selection():
    team1_index = team1_listbox.curselection()

    if not team1_index:
        messagebox.showerror("Error", "Please select a team for Team 1.")
        return

    current_game.add_home_team(teams[team1_index[0]])

    team1_selection_frame.grid_forget()
    team2_listbox.delete(0, tk.END)
    for team in teams:
        if team.name != current_game.get_teams()[0]:
            team2_listbox.insert(tk.END, team.name)

    team2_selection_frame.grid(row=0, column=0, columnspan=2, pady=10)


def handle_team2_selection():
    team2_index = team2_listbox.curselection()

    if not team2_index:
        messagebox.showerror("Error", "Please select a team for Team 2.")
        return

    current_game.add_away_team(teams[team2_index[0]])

    if current_game.get_teams()[0] == current_game.get_teams()[1]:
        messagebox.showerror("Error", "Team 2 cannot be the same as Team 1.")
        return

    update_selected_teams_label()

    team2_selection_frame.grid_forget()
    event_type_frame.grid(row=1, column=0, columnspan=2, pady=10)

    event_list_frame.grid(row=3, column=0, columnspan=2, pady=10)


def show_event_form(event_type):
    selected_event_type.set(event_type)
    for widget in event_form_frame.winfo_children():
        widget.destroy()

    update_selected_teams_label()

    tk.Label(event_form_frame, text=f"Selected Event Type: {event_type}").grid(
        row=1, column=0, columnspan=2, pady=10)

    tk.Label(event_form_frame, text="Event Content:").grid(
        row=2, column=0, padx=10, pady=10)
    global event_content_entry
    event_content_entry = tk.Entry(event_form_frame)
    event_content_entry.grid(row=2, column=1, padx=10, pady=10)

    add_event_button = tk.Button(
        event_form_frame, text="Add Event", command=handle_add_event)
    add_event_button.grid(row=3, column=0, columnspan=2, pady=20)

    event_form_frame.grid(row=2, column=0, columnspan=2, pady=10)


def update_selected_teams_label():
    """Update the label to display the selected teams."""  # Initially hidden
    global selected_teams_label
    selected_teams_label.config(
        text=f"Selected Teams: {current_game.get_teams()[0]} vs {current_game.get_teams()[1]}"
    )


root = tk.Tk()
root.title("Scorekeeper")

start_game_frame = tk.Frame(root)
start_game_frame.grid(row=0, column=0, columnspan=2, pady=10)

tk.Label(start_game_frame, text="Welcome to Scorekeeper!", font=("Arial", 16)).grid(
    row=0, column=0, columnspan=2, pady=10
)
start_game_button = tk.Button(
    start_game_frame, text="Start a New Game", font=("Arial", 14), command=start_new_game
)
start_game_button.grid(row=1, column=0, columnspan=2, pady=20)

selected_teams_label = tk.Label(root, text="", font=("Arial", 14))
selected_teams_label.grid(row=0, column=0, columnspan=2, pady=10)

team1_selection_frame = tk.Frame(root)

tk.Label(team1_selection_frame, text="Select Team 1:").grid(
    row=0, column=0, padx=10, pady=10
)
team1_listbox = tk.Listbox(team1_selection_frame, height=5)
team1_listbox.grid(row=1, column=0, padx=10, pady=10)
for team in teams:
    team1_listbox.insert(tk.END, team.name)

select_team1_button = tk.Button(
    team1_selection_frame, text="Select Team 1", command=handle_team1_selection
)
select_team1_button.grid(row=2, column=0, pady=20)

team2_selection_frame = tk.Frame(root)

tk.Label(team2_selection_frame, text="Select Team 2:").grid(
    row=0, column=0, padx=10, pady=10
)
team2_listbox = tk.Listbox(team2_selection_frame, height=5)
team2_listbox.grid(row=1, column=0, padx=10, pady=10)
for team in teams:
    team2_listbox.insert(tk.END, team.name)

select_team2_button = tk.Button(
    team2_selection_frame, text="Select Team 2", command=handle_team2_selection
)
select_team2_button.grid(row=2, column=0, pady=20)

event_type_frame = tk.Frame(root)

tk.Label(event_type_frame, text="Select Event Type:").grid(
    row=1, column=0, columnspan=2, pady=10
)

selected_event_type = tk.StringVar()

for i, event_type in enumerate(EVENT_TYPES):
    tk.Button(
        event_type_frame,
        text=event_type,
        command=lambda et=event_type: show_event_form(et),
    ).grid(row=2, column=i, padx=10, pady=10)

event_form_frame = tk.Frame(root)

event_list_frame = tk.Frame(root)
event_list_frame.grid_forget()

tk.Label(event_list_frame, text="Added Events:").grid(
    row=0, column=0, columnspan=2, pady=10)
event_listbox = tk.Listbox(event_list_frame, width=40, height=10)
event_listbox.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

update_event_list()

root.mainloop()
