import tkinter as tk
from tkinter import ttk, messagebox


class TeamSelectionView:
    def __init__(self, root, score_service, handle_selection):
        """Initialize team selection view.

        Args:
            root: Tkinter root window
            score_service: ScoreService instance
            handle_selection: Callback for team selection
        """
        self._root = root
        self._score_service = score_service
        self._handle_selection = handle_selection
        self._frame = None
        self._team1_var = None
        self._team2_var = None
        self._initialize()

    def _initialize(self):
        """Set up the team selection view."""
        self._frame = ttk.Frame(self._root)

        # Header
        header_label = ttk.Label(
            self._frame,
            text="Select Teams",
            font=("Arial", 16, "bold")
        )
        header_label.grid(row=0, column=0, columnspan=2, pady=20)

        # Team 1 selection
        ttk.Label(self._frame, text="Home Team:").grid(
            row=1, column=0, padx=5, pady=5)
        self._team1_var = tk.StringVar()
        team1_menu = ttk.Combobox(
            self._frame,
            textvariable=self._team1_var,
            values=[team.name for team in self._score_service.get_teams()],
            state="readonly"
        )
        team1_menu.grid(row=1, column=1, padx=5, pady=5)

        # Team 2 selection
        ttk.Label(self._frame, text="Away Team:").grid(
            row=2, column=0, padx=5, pady=5)
        self._team2_var = tk.StringVar()
        team2_menu = ttk.Combobox(
            self._frame,
            textvariable=self._team2_var,
            values=[team.name for team in self._score_service.get_teams()],
            state="readonly"
        )
        team2_menu.grid(row=2, column=1, padx=5, pady=5)

        # Continue button
        ttk.Button(
            self._frame,
            text="Continue",
            command=self._handle_team_selection
        ).grid(row=3, column=0, columnspan=2, pady=20)

        self._frame.pack(padx=20, pady=20)

    def _handle_team_selection(self):
        """Validate and process team selection."""
        team1 = self._team1_var.get()
        team2 = self._team2_var.get()

        if not team1 or not team2:
            messagebox.showerror("Error", "Please select both teams")
            return

        if team1 == team2:
            messagebox.showerror("Error", "Please select different teams")
            return

        # Start new game with selected teams
        self._score_service.start_new_game()
        self._handle_selection()

    def destroy(self):
        """Destroy this view."""
        self._frame.destroy()
