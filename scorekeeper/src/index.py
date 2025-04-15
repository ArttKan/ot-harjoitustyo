import tkinter as tk
from tkinter import messagebox
from services.score_service import ScoreService
from entities.team import Team
from entities.player import Player
from entities.game import Game
from entities.event import Event


Scorekeeper = ScoreService()
current_game = None

EVENT_TYPES = ["2-Pointer", "3-Pointer", "Rebound", "Foul", "Technical Foul"]

team1 = Team("Golden State Warriors")
team2 = Team("Los Angeles Lakers")
team1.add_player(Player("Stephen Curry", 30))
team1.add_player(Player("Draymond Green", 23))
team2.add_player(Player("Luka Doncic", 77))
team2.add_player(Player("LeBron James", 6))
teams = [team1, team2]
remaining_teams = []

root = None
selected_event_type = None
event_content_entry = None

# Frames
start_game_frame = None
team1_selection_frame = None
team2_selection_frame = None
player_selection_frame = None
event_type_frame = None
event_form_frame = None
event_list_frame = None

# Listboxes
team1_listbox = None
team2_listbox = None
event_listbox = None


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

    selected_team1 = teams[team1_index[0]]
    current_game.add_home_team(selected_team1)

    team1_selection_frame.grid_forget()

    # Create a list of remaining teams
    global remaining_teams
    remaining_teams = [team for team in teams if team != selected_team1]

    # Update team2_listbox with only remaining teams
    team2_listbox.delete(0, tk.END)
    for team in remaining_teams:
        team2_listbox.insert(tk.END, team.name)

    team2_selection_frame.grid(row=0, column=0, columnspan=2, pady=10)


def handle_team2_selection():
    team2_index = team2_listbox.curselection()

    if not team2_index:
        messagebox.showerror("Error", "Please select a team for Team 2.")
        return

    # Use the remaining_teams list to get the correct team
    selected_team2 = remaining_teams[team2_index[0]]
    current_game.add_away_team(selected_team2)

    if current_game.get_team_names()[0] == current_game.get_team_names()[1]:
        messagebox.showerror("Error", "Team 2 cannot be the same as Team 1.")
        return

    team2_selection_frame.grid_forget()

    # Update and show player selection frame
    update_player_frame()
    player_selection_frame.grid(row=1, column=0, columnspan=2, pady=10)


def setup_player_selection_frame():
    """Initialize and configure the player selection frame."""
    frame = tk.Frame(root)
    continue_button = None  # Define button at function scope

    def update_continue_button_state():
        """Update the continue button state based on player counts."""
        if not current_game or not current_game.get_teams():
            return
        team1_players = len(current_game.get_teams()[0].get_players())
        team2_players = len(current_game.get_teams()[1].get_players())

        if team1_players > 0 and team2_players > 0:
            continue_button.config(state=tk.NORMAL)
        else:
            continue_button.config(state=tk.DISABLED)

    def add_player_to_team(team, name_entry, number_entry, error_label, listbox):
        """Add player to team and update continue button."""
        validate_and_add_player(
            team, name_entry, number_entry, error_label, listbox)
        update_continue_button_state()

    def update_player_frame():
        """Update the player frame with current game teams."""
        if not current_game or not current_game.get_teams():
            return frame

        # Team 1 Players
        team1_players_frame = tk.Frame(frame)
        team1_players_frame.grid(row=0, column=0, padx=20, pady=10)

        tk.Label(team1_players_frame,
                 text=f"{current_game.get_teams()[0].name} Players",
                 font=("Arial", 12, "bold")).grid(row=0, column=0, pady=5, columnspan=2)

        team1_player_listbox = tk.Listbox(
            team1_players_frame, height=10, width=30)
        team1_player_listbox.grid(row=1, column=0, pady=5, columnspan=2)

        # Team 1 Player Input Fields
        tk.Label(team1_players_frame, text="Name:").grid(
            row=2, column=0, pady=5)
        name_entry1 = tk.Entry(team1_players_frame)
        name_entry1.grid(row=2, column=1, pady=5)

        tk.Label(team1_players_frame, text="Number:").grid(
            row=3, column=0, pady=5)
        number_entry1 = tk.Entry(team1_players_frame)
        number_entry1.grid(row=3, column=1, pady=5)

        error_label1 = tk.Label(team1_players_frame, text="", fg="red")
        error_label1.grid(row=4, column=0, columnspan=2, pady=5)

        add_player1_button = tk.Button(
            team1_players_frame,
            text="Add Player",
            command=lambda: add_player_to_team(
                current_game.get_teams()[0],
                name_entry1,
                number_entry1,
                error_label1,
                team1_player_listbox
            )
        )
        add_player1_button.grid(row=5, column=0, columnspan=2, pady=5)

        # Team 2 Players
        team2_players_frame = tk.Frame(frame)
        team2_players_frame.grid(row=0, column=1, padx=20, pady=10)

        tk.Label(team2_players_frame,
                 text=f"{current_game.get_teams()[1].name} Players",
                 font=("Arial", 12, "bold")).grid(row=0, column=0, pady=5, columnspan=2)

        team2_player_listbox = tk.Listbox(
            team2_players_frame, height=10, width=30)
        team2_player_listbox.grid(row=1, column=0, pady=5, columnspan=2)

        # Team 2 Player Input Fields
        tk.Label(team2_players_frame, text="Name:").grid(
            row=2, column=0, pady=5)
        name_entry2 = tk.Entry(team2_players_frame)
        name_entry2.grid(row=2, column=1, pady=5)

        tk.Label(team2_players_frame, text="Number:").grid(
            row=3, column=0, pady=5)
        number_entry2 = tk.Entry(team2_players_frame)
        number_entry2.grid(row=3, column=1, pady=5)

        error_label2 = tk.Label(team2_players_frame, text="", fg="red")
        error_label2.grid(row=4, column=0, columnspan=2, pady=5)

        add_player2_button = tk.Button(
            team2_players_frame,
            text="Add Player",
            command=lambda: add_player_to_team(
                current_game.get_teams()[1],
                name_entry2,
                number_entry2,
                error_label2,
                team2_player_listbox
            )
        )
        add_player2_button.grid(row=5, column=0, columnspan=2, pady=5)

        # Continue button
        nonlocal continue_button
        continue_button = tk.Button(
            frame,
            text="Continue to Game",
            command=lambda: continue_to_game(frame),
            state=tk.DISABLED
        )
        continue_button.grid(row=1, column=0, columnspan=2, pady=20)

        update_continue_button_state()

        # Show any existing players
        for player in current_game.get_teams()[0].get_players():
            team1_player_listbox.insert(
                tk.END, f"#{player.number:02d} {player.name}")
        for player in current_game.get_teams()[1].get_players():
            team2_player_listbox.insert(
                tk.END, f"#{player.number:02d} {player.name}")

    return frame, update_player_frame


def validate_and_add_player(team, name_entry, number_entry, error_label, listbox):
    """Validate and add a player to the team."""
    # Validate name
    name = name_entry.get().strip()

    if len(name) < 4 or not all(c.isalpha() or c.isspace() for c in name):
        error_label.config(
            text="Name must be at least 4 characters long and contain only letters and spaces")
        return

    # Check that name isn't just spaces
    if not any(c.isalpha() for c in name):
        error_label.config(text="Name must contain at least one letter")
        return

    # Validate number
    number = number_entry.get().strip()
    try:
        num = int(number)
        if num < 0 or num > 99:
            error_label.config(text="Number must be between 00 and 99")
            return
    except ValueError:
        error_label.config(text="Number must be between 00 and 99")
        return

    # Check for duplicate name
    for player in team.get_players():
        if player.name.lower() == name.lower():
            error_label.config(
                text=f"Player with name {name} already exists in the team")
            return

    # Check for duplicate number
    number = number.zfill(2)  # Pad with leading zero if needed
    for player in team.get_players():
        if str(player.number).zfill(2) == number:
            error_label.config(
                text=f"Player with number {number} already exists in the team")
            return

    # Add player
    new_player = Player(name, int(number))
    team.add_player(new_player)
    listbox.insert(tk.END, f"#{number} {name}")

    # Clear inputs and error message
    name_entry.delete(0, tk.END)
    number_entry.delete(0, tk.END)
    error_label.config(text="")


def continue_to_game(player_frame):
    """Transition from player selection to game events."""
    player_frame.grid_forget()

    # Clear any existing content
    if event_form_frame:
        event_form_frame.grid_forget()
    if event_type_frame:
        event_type_frame.grid_forget()
    if event_list_frame:
        event_list_frame.grid_forget()

    # Row 0: Game info header
    game_info_frame = tk.Frame(root)
    game_info_frame.grid(row=0, column=0, columnspan=2, pady=10, sticky="ew")
    game_info_frame.grid_columnconfigure(1, weight=1)

    # Add teams and score
    team1_name = current_game.get_team_names()[0]
    team2_name = current_game.get_team_names()[1]

    global score_label  # Add this at the top of the file with other globals
    score_label = tk.Label(game_info_frame, text="0 - 0",
                           font=("Arial", 14, "bold"))
    score_label.grid(row=0, column=1, padx=20)

    tk.Label(game_info_frame, text=team1_name, font=("Arial", 14, "bold")).grid(
        row=0, column=0, padx=20)
    score_label.grid(row=0, column=1, padx=20)
    tk.Label(game_info_frame, text=team2_name, font=("Arial", 14, "bold")).grid(
        row=0, column=2, padx=20)

    # Row 1: Player lists
    players_frame = tk.Frame(root)
    players_frame.grid(row=1, column=0, columnspan=2, pady=10)

    # Team 1 players
    team1_frame = tk.Frame(players_frame)
    team1_frame.grid(row=0, column=0, padx=20)
    tk.Label(team1_frame, text="Players", font=("Arial", 12, "bold")).grid(
        row=0, column=0)
    team1_players = tk.Listbox(team1_frame, height=10, width=25)
    team1_players.grid(row=1, column=0, pady=5)
    for player in current_game.get_teams()[0].get_players():
        team1_players.insert(tk.END, f"#{player.number:02d} {player.name}")

    # Team 2 players
    team2_frame = tk.Frame(players_frame)
    team2_frame.grid(row=0, column=1, padx=20)
    tk.Label(team2_frame, text="Players", font=("Arial", 12, "bold")).grid(
        row=0, column=0)
    team2_players = tk.Listbox(team2_frame, height=10, width=25)
    team2_players.grid(row=1, column=0, pady=5)
    for player in current_game.get_teams()[1].get_players():
        team2_players.insert(tk.END, f"#{player.number:02d} {player.name}")

    # Row 2: Event type buttons
    event_type_frame.grid(row=2, column=0, columnspan=2, pady=10)
    setup_event_type_frame()

    # Row 4: Event list (row 3 reserved for event form)
    event_list_frame.grid(row=4, column=0, columnspan=2, pady=10)


def update_score_display():
    """Update the score display with current scores."""
    team1_name = current_game.get_team_names()[0]
    team2_name = current_game.get_team_names()[1]

    team1_score = Scorekeeper.get_team_score(team1_name)
    team2_score = Scorekeeper.get_team_score(team2_name)

    score_label.config(text=f"{team1_score} - {team2_score}")


def setup_event_type_frame():
    """Initialize and configure the event type selection frame."""
    # Clear existing widgets
    for widget in event_type_frame.winfo_children():
        widget.destroy()

    tk.Label(event_type_frame, text="Select Event Type:").grid(
        row=0, column=0, columnspan=len(EVENT_TYPES), pady=10
    )

    for i, event_type in enumerate(EVENT_TYPES):
        tk.Button(
            event_type_frame,
            text=event_type,
            command=lambda et=event_type: show_event_form(et),
        ).grid(row=1, column=i, padx=10, pady=10)

    return event_type_frame


def handle_event_confirmation(event_type, team, player):
    """Handle the confirmation of an event."""
    event = Event(event_type, player, team)
    Scorekeeper.add_event(event)

    messagebox.showinfo("Success", f"{event_type} added for {player.name}")

    # Hide the event form
    event_form_frame.grid_forget()

    # Update the event list and score display
    update_event_list()
    update_score_display()


def update_event_list():
    """Update the event list to show event type, player and team."""
    event_listbox.delete(0, tk.END)
    events = Scorekeeper.get_events()
    for event in events:
        event_listbox.insert(tk.END,
                             f"{event.type} - {event.player.name} ({event.team.name})")


def show_event_confirmation(input_frame, event_type, team, player):
    """Show the final event confirmation screen."""
    # Clear previous content
    for widget in input_frame.winfo_children():
        widget.destroy()

    # Show event summary
    tk.Label(input_frame,
             text=f"Selected Event: {event_type}",
             font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=5)

    tk.Label(input_frame,
             text=f"Team: {team.name}",
             font=("Arial", 11)).grid(row=1, column=0, columnspan=2, pady=5)

    tk.Label(input_frame,
             text=f"Player: #{player.number:02d} {player.name}",
             font=("Arial", 11)).grid(row=2, column=0, columnspan=2, pady=5)

    tk.Button(input_frame,
              text="Confirm Event",
              command=lambda: handle_event_confirmation(event_type, team, player)).grid(
        row=3, column=0, columnspan=2, pady=10)


def show_player_selection(input_frame, event_type, team):
    """Show player selection screen."""
    # Clear previous content
    for widget in input_frame.winfo_children():
        widget.destroy()

    tk.Label(input_frame,
             text=f"Selected Event: {event_type}",
             font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=5)

    tk.Label(input_frame,
             text=f"Team: {team.name}",
             font=("Arial", 11)).grid(row=1, column=0, columnspan=2, pady=5)

    tk.Label(input_frame, text="Select Player:").grid(
        row=2, column=0, columnspan=2, pady=5)

    player_listbox = tk.Listbox(input_frame, height=5, width=30)
    player_listbox.grid(row=3, column=0, columnspan=2, pady=5)

    for player in team.get_players():
        player_listbox.insert(tk.END, f"#{player.number:02d} {player.name}")

    def on_player_selected():
        selection = player_listbox.curselection()
        if not selection:
            messagebox.showerror("Error", "Please select a player")
            return
        selected_player = team.get_players()[selection[0]]
        show_event_confirmation(input_frame, event_type, team, selected_player)

    tk.Button(input_frame,
              text="Continue",
              command=on_player_selected).grid(row=4, column=0, columnspan=2, pady=10)


def show_event_form(event_type):
    """Show initial event form with team selection."""
    global event_form_frame, selected_event_type

    # Store selected event type
    selected_event_type = tk.StringVar(value=event_type)

    # Create or clear event form frame
    if not event_form_frame:
        event_form_frame = tk.Frame(root)
    else:
        for widget in event_form_frame.winfo_children():
            widget.destroy()

    # Configure columns for centering
    event_form_frame.grid_columnconfigure(0, weight=1)
    event_form_frame.grid_columnconfigure(1, weight=0)
    event_form_frame.grid_columnconfigure(2, weight=1)

    # Team selection frame
    input_frame = tk.Frame(event_form_frame)
    input_frame.grid(row=0, column=1, pady=10)

    # Add team selection buttons
    tk.Label(input_frame,
             text=f"Selected Event: {event_type}",
             font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=5)

    tk.Label(input_frame, text="Select Team:").grid(
        row=1, column=0, columnspan=2, pady=5)

    team_frame = tk.Frame(input_frame)
    team_frame.grid(row=2, column=0, columnspan=2, pady=5)

    team1, team2 = current_game.get_teams()
    tk.Button(team_frame,
              text=team1.name,
              command=lambda: show_player_selection(input_frame, event_type, team1)).grid(
        row=0, column=0, padx=10)

    tk.Button(team_frame,
              text=team2.name,
              command=lambda: show_player_selection(input_frame, event_type, team2)).grid(
        row=0, column=1, padx=10)

    # Display the event form frame
    event_form_frame.grid(row=3, column=0, columnspan=2, pady=10, sticky="ew")


def handle_add_event():
    """Handle adding an event and hide the input form."""
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

    # Hide the event form after successful addition
    event_form_frame.grid_forget()

    # Clear the entry for next use
    event_content_entry.delete(0, tk.END)

    update_event_list()


def setup_start_game_frame():
    """Initialize and configure the start game frame."""
    frame = tk.Frame(root)
    frame.grid(row=0, column=0, columnspan=2, pady=10)

    tk.Label(frame, text="Welcome to Scorekeeper!", font=("Arial", 16)).grid(
        row=0, column=0, columnspan=2, pady=10
    )
    start_game_button = tk.Button(
        frame, text="Start a New Game", font=("Arial", 14), command=start_new_game
    )
    start_game_button.grid(row=1, column=0, columnspan=2, pady=20)
    return frame


def setup_team_selection_frames():
    """Initialize and configure team selection frames."""
    # Team 1 Frame
    team1_frame = tk.Frame(root)
    tk.Label(team1_frame, text="Select Team 1:").grid(
        row=0, column=0, padx=10, pady=10
    )
    team1_listbox = tk.Listbox(team1_frame, height=5)
    team1_listbox.grid(row=1, column=0, padx=10, pady=10)
    for team in teams:
        team1_listbox.insert(tk.END, team.name)

    select_team1_button = tk.Button(
        team1_frame, text="Select Team 1", command=handle_team1_selection
    )
    select_team1_button.grid(row=2, column=0, pady=20)

    # Team 2 Frame
    team2_frame = tk.Frame(root)
    tk.Label(team2_frame, text="Select Team 2:").grid(
        row=0, column=0, padx=10, pady=10
    )
    team2_listbox = tk.Listbox(team2_frame, height=5)
    team2_listbox.grid(row=1, column=0, padx=10, pady=10)
    for team in teams:
        team2_listbox.insert(tk.END, team.name)

    select_team2_button = tk.Button(
        team2_frame, text="Select Team 2", command=handle_team2_selection
    )
    select_team2_button.grid(row=2, column=0, pady=20)

    return team1_frame, team1_listbox, team2_frame, team2_listbox


def setup_event_list_frame():
    """Initialize and configure the event list frame."""
    frame = tk.Frame(root)
    tk.Label(frame, text="Added Events:").grid(
        row=0, column=0, columnspan=2, pady=10)
    listbox = tk.Listbox(frame, width=40, height=10)
    listbox.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
    frame.grid_forget()
    return frame, listbox


def initialize_ui():
    """Initialize all UI components."""
    global root, start_game_frame, team1_selection_frame, team2_selection_frame
    global team1_listbox, team2_listbox, event_type_frame, event_form_frame
    global event_list_frame, event_listbox, player_selection_frame
    global update_player_frame

    # Clear any existing windows/frames
    if root:
        root.destroy()

    root = tk.Tk()
    root.title("Scorekeeper")

    # Initialize frames as None first
    event_form_frame = tk.Frame(root)
    event_type_frame = tk.Frame(root)

    # Setup all frames
    start_game_frame = setup_start_game_frame()
    team1_selection_frame, team1_listbox, team2_selection_frame, team2_listbox = setup_team_selection_frames()
    player_selection_frame, update_player_frame = setup_player_selection_frame()
    event_type_frame = setup_event_type_frame()
    event_form_frame = tk.Frame(root)
    event_list_frame, event_listbox = setup_event_list_frame()

    update_event_list()


if __name__ == "__main__":
    initialize_ui()
    root.mainloop()
