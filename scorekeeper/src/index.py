import tkinter as tk
from tkinter import messagebox
from services.score_service import ScoreService
from entities.team import Team
from entities.player import Player

Scorekeeper = ScoreService()

# Predetermined event types

EVENT_TYPES = ["2-Pointer", "3-Pointer", "Rebound", "Foul", "Technical Foul"]
team1 = Team("Golden State Warriors")
team2 = Team("Los Angeles Lakers")
team1.add_player(Player("Stephen Curry"))
team1.add_player(Player("Draymond Green"))
team2.add_player(Player("Luka Doncic"))
team2.add_player(Player("LeBron James"))
teams = [team1, team2]

# Function to handle adding an event


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

# Function to update the event list


def update_event_list():
    event_listbox.delete(0, tk.END)
    events = Scorekeeper.get_events()
    for event in events:
        event_listbox.insert(tk.END, f"{event.type} - Score: {event.content}")

# Function to show the input form for the selected event type


def show_event_form(event_type):
    selected_event_type.set(event_type)
    for widget in event_type_frame.winfo_children():
        widget.destroy()

    tk.Label(event_type_frame, text=f"Selected Event Type: {event_type}").grid(
        row=0, column=0, columnspan=2, pady=10)

    tk.Label(event_type_frame, text="Event Content:").grid(
        row=1, column=0, padx=10, pady=10)
    global event_content_entry
    event_content_entry = tk.Entry(event_type_frame)
    event_content_entry.grid(row=1, column=1, padx=10, pady=10)

    add_event_button = tk.Button(
        event_type_frame, text="Add Event", command=handle_add_event)
    add_event_button.grid(row=2, column=0, columnspan=2, pady=20)


def handle_team1_selection():
    global selected_team1
    team1_index = team1_listbox.curselection()

    # Validate that a team is selected
    if not team1_index:
        messagebox.showerror("Error", "Please select a team for Team 1.")
        return

    # Retrieve the selected team
    selected_team1 = teams[team1_index[0]]

    # Proceed to Team 2 selection
    team1_selection_frame.grid_forget()
    team2_selection_frame.grid(row=0, column=0, columnspan=2, pady=10)


def handle_team2_selection():
    global selected_team2
    team2_index = team2_listbox.curselection()

    # Validate that a team is selected
    if not team2_index:
        messagebox.showerror("Error", "Please select a team for Team 2.")
        return

    # Retrieve the selected team
    selected_team2 = teams[team2_index[0]]

    # Validate that Team 2 is not the same as Team 1
    if selected_team1 == selected_team2:
        messagebox.showerror("Error", "Team 2 cannot be the same as Team 1.")
        return

    # Proceed to event type selection
    team2_selection_frame.grid_forget()
    event_type_frame.grid(row=0, column=0, columnspan=2, pady=10)


# Create the main tkinter window
root = tk.Tk()
root.title("Scorekeeper")

# Frame for Team 1 selection
team1_selection_frame = tk.Frame(root)
team1_selection_frame.grid(row=0, column=0, columnspan=2, pady=10)

tk.Label(team1_selection_frame, text="Select Team 1:").grid(
    row=0, column=0, padx=10, pady=10)
team1_listbox = tk.Listbox(team1_selection_frame, height=5)
team1_listbox.grid(row=1, column=0, padx=10, pady=10)
for team in teams:
    team1_listbox.insert(tk.END, team.name)

select_team1_button = tk.Button(
    team1_selection_frame, text="Select Team 1", command=handle_team1_selection)
select_team1_button.grid(row=2, column=0, pady=20)

# Frame for Team 2 selection (hidden initially)
team2_selection_frame = tk.Frame(root)

tk.Label(team2_selection_frame, text="Select Team 2:").grid(
    row=0, column=0, padx=10, pady=10)
team2_listbox = tk.Listbox(team2_selection_frame, height=5)
team2_listbox.grid(row=1, column=0, padx=10, pady=10)
for team in teams:
    team2_listbox.insert(tk.END, team.name)

select_team2_button = tk.Button(
    team2_selection_frame, text="Select Team 2", command=handle_team2_selection)
select_team2_button.grid(row=2, column=0, pady=20)

# Frame for event type selection (hidden initially)
event_type_frame = tk.Frame(root)

tk.Label(event_type_frame, text="Select Event Type:").grid(
    row=0, column=0, columnspan=2, pady=10)

selected_event_type = tk.StringVar()

for i, event_type in enumerate(EVENT_TYPES):
    tk.Button(event_type_frame, text=event_type, command=lambda et=event_type: show_event_form(
        et)).grid(row=1, column=i, padx=10, pady=10)

# Frame for the event input form
event_form_frame = tk.Frame(root)

# Frame for the event list
tk.Label(root, text="Added Events:").grid(
    row=2, column=0, columnspan=2, pady=10)
event_listbox = tk.Listbox(root, width=40, height=10)
event_listbox.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

update_event_list()

root.mainloop()
