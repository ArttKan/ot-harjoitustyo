import tkinter as tk
from tkinter import ttk, messagebox


class TeamSelectionView:
    def __init__(self, root, score_service, handle_selection):
        """Initialize team selection view."""
        self._root = root
        self._score_service = score_service
        self._handle_selection = handle_selection
        self._frame = None
        self._team1_entry = None
        self._team2_entry = None
        self._initialize()

    def _initialize(self):
        """Set up the team selection view."""
        self._frame = ttk.Frame(self._root)

        header_label = ttk.Label(
            self._frame,
            text="Enter Team Names",
            font=("Arial", 16, "bold")
        )
        header_label.grid(row=0, column=0, columnspan=2, pady=20)

        ttk.Label(self._frame, text="Home Team:").grid(
            row=1, column=0, padx=5, pady=5)
        self._team1_entry = ttk.Entry(self._frame)
        self._team1_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self._frame, text="Away Team:").grid(
            row=2, column=0, padx=5, pady=5)
        self._team2_entry = ttk.Entry(self._frame)
        self._team2_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Button(
            self._frame,
            text="Continue",
            command=self._handle_team_selection
        ).grid(row=3, column=0, columnspan=2, pady=20)

        self._frame.pack(padx=20, pady=20)

    def _handle_team_selection(self):
        """Validate and process team selection."""
        team1 = self._team1_entry.get().strip()
        team2 = self._team2_entry.get().strip()

        if not team1 or not team2:
            messagebox.showerror("Error", "Please enter both team names")
            return

        if team1 == team2:
            messagebox.showerror("Error", "Please enter different team names")
            return

        try:
            self._score_service.start_new_game(team1, team2)
            self._handle_selection()
        except ValueError as error:
            messagebox.showerror("Error", str(error))

    def destroy(self):
        """Destroy this view."""
        self._frame.destroy()
