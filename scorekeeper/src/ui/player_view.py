import tkinter as tk
from tkinter import ttk, messagebox
from repositories.player_repository import PlayerRepository


class PlayerView:
    def __init__(self, root, score_service, handle_next):
        """Initialize player management view.

        Args:
            root: Tkinter root window
            score_service: ScoreService instance
            handle_next: Callback for navigation
        """
        self._root = root
        self._score_service = score_service
        self._handle_next = handle_next
        self._frame = None
        self._player_listbox = None
        self._initialize()

    def _initialize(self):
        """Set up the player management view."""
        self._frame = ttk.Frame(self._root)

        header_label = ttk.Label(
            self._frame,
            text="Team Rosters",
            font=("Arial", 16, "bold")
        )
        header_label.grid(row=0, column=0, columnspan=3, pady=20)

        player_frame = ttk.LabelFrame(self._frame)
        player_frame.grid(row=1, column=0, columnspan=3,
                          padx=10, pady=5, sticky="nsew")

        self._player_listbox = tk.Listbox(player_frame, width=40, height=10)
        self._player_listbox.pack(padx=10, pady=5)
        self._update_player_list()

        add_frame = ttk.LabelFrame(self._frame, text="Add New Player")
        add_frame.grid(row=2, column=0, columnspan=3,
                       padx=10, pady=5, sticky="nsew")

        ttk.Label(add_frame, text="Team:").grid(
            row=0, column=0, padx=5, pady=5)
        self._team_var = tk.StringVar()
        team_dropdown = ttk.Combobox(
            add_frame,
            textvariable=self._team_var,
            state="readonly"
        )
        current_game = self._score_service.get_current_game()
        if current_game:
            teams = current_game.get_teams()
            team_dropdown['values'] = [team.name for team in teams]
            if teams:
                team_dropdown.set(teams[0].name)
        team_dropdown.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(add_frame, text="Name (A-Z and spaces):").grid(
            row=1, column=0, padx=5, pady=5)
        name_entry = ttk.Entry(add_frame)
        name_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(add_frame, text="Number (0-99):").grid(
            row=2, column=0, padx=5, pady=5)
        number_entry = ttk.Entry(add_frame)
        number_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Button(
            add_frame,
            text="Add Player",
            command=lambda: self._add_player(name_entry, number_entry)
        ).grid(row=3, column=0, columnspan=2, pady=10)

        button_frame = ttk.Frame(self._frame)
        button_frame.grid(row=3, column=0, columnspan=3, pady=20)

        self._continue_button = ttk.Button(
            button_frame,
            text="Continue to Game",
            command=self._handle_next
        )
        self._continue_button.pack(side=tk.RIGHT, padx=5)

        self._update_continue_button_state()

        self._frame.pack(padx=20, pady=20)

    def _update_player_list(self):
        """Update the player list display."""
        self._player_listbox.delete(0, tk.END)
        current_game = self._score_service.get_current_game()
        if current_game:
            for team in current_game.get_teams():
                self._player_listbox.insert(tk.END, f"=== {team.name} ===")
                for player in team.get_players():
                    self._player_listbox.insert(
                        tk.END,
                        f"#{player.number:02d} {player.name}"
                    )
                self._player_listbox.insert(tk.END, "")

    def _add_player(self, name_entry, number_entry):
        """Add a new player to the selected team."""
        try:
            name = name_entry.get().strip()
            try:
                number = int(number_entry.get().strip())
            except ValueError:
                raise ValueError("Enter a valid number as player number")
                
            selected_team = self._team_var.get()
            if not selected_team:
                raise ValueError("Select a team first")

            # Use the validation function
            is_valid, error_message = self._validate_player(name, number, selected_team)
            if not is_valid:
                raise ValueError(error_message)

            current_game = self._score_service.get_current_game()
            if current_game:
                team = next((t for t in current_game.get_teams()
                            if t.name == selected_team), None)
                if team:
                    self._score_service.add_player(team, name, number)
                    name_entry.delete(0, tk.END)
                    number_entry.delete(0, tk.END)
                    self._update_player_list()
                    self._update_continue_button_state()

        except ValueError as error:
            messagebox.showerror("Error", str(error))

    def _validate_player(self, name, number, team_name):
        """Validate player input.

        Args:
            name (str): Player name to validate
            number (int): Player number to validate

        Returns:
            tuple: (bool, str) - (is_valid, error_message)
        """
        if not name:
            return False, "Enter a player name and number"

        if len(name) < 3:
            return False, "Player name must be at least 3 characters long"

        test_name = name.replace(" ", "")
        if not test_name.isalpha():
            return False, "Only alphabetical characters and spaces allowed in player names"

        if not number:
            return False, "Enter a player name and number"

        if number < 0 or number > 99:
            return False, "Number must be between 0 and 99"
        current_game = self._score_service.get_current_game()
        if current_game:
            for player in self._score_service.get_team_players(team_name):
                if player.name.lower() == name.lower():
                    return False, f"Player with name {name} already exists"
                if player.number == number:
                    return False, f"Player with number {number} already exists"

        return True, ""

    def _update_continue_button_state(self):
        """Enable/disable continue button based on player counts."""
        current_game = self._score_service.get_current_game()
        if not current_game:
            return

        teams = current_game.get_teams()
        if not all(len(team.get_players()) > 0 for team in teams):
            self._continue_button.config(state="disabled")
        else:
            self._continue_button.config(state="normal")

    def destroy(self):
        """Destroy this view."""
        self._frame.destroy()
