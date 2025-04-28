import tkinter as tk
from tkinter import messagebox
from services.score_service import ScoreService
from entities.team import Team
from entities.player import Player
from entities.game import Game
from entities.event import Event


class ScoreKeeperUI:
    def __init__(self):
        self.scorekeeper = ScoreService()
        self.current_game = None
        self.event_types = ["2-Pointer", "3-Pointer",
                            "Rebound", "Foul", "Technical Foul"]

        # Initialize demo data
        team1 = Team("Golden State Warriors")
        team2 = Team("Los Angeles Lakers")
        team1.add_player(Player("Stephen Curry", 30))
        team1.add_player(Player("Draymond Green", 23))
        team2.add_player(Player("Luka Doncic", 77))
        team2.add_player(Player("LeBron James", 6))
        self.teams = [team1, team2]
        self.remaining_teams = []

        # Initialize UI elements
        self.root = None
        self.selected_event_type = None
        self.score_label = None

        # Frames
        self.start_game_frame = None
        self.team1_selection_frame = None
        self.team2_selection_frame = None
        self.player_selection_frame = None
        self.event_type_frame = None
        self.event_form_frame = None
        self.event_list_frame = None

        # Listboxes
        self.team1_listbox = None
        self.team2_listbox = None
        self.event_listbox = None

    def initialize_ui(self):
        """Initialize all UI components."""
        if self.root:
            self.root.destroy()

        self.root = tk.Tk()
        self.root.title("Scorekeeper")

        # Initialize frames
        self.event_form_frame = tk.Frame(self.root)
        self.event_type_frame = tk.Frame(self.root)

        # Setup all frames
        self.start_game_frame = self.setup_start_game_frame()
        self.setup_team_selection_frames()
        self.setup_player_selection_frame()
        self.setup_event_type_frame()
        self.setup_event_list_frame()

        self.update_event_list()

    def start(self):
        """Start the UI."""
        self.initialize_ui()
        self.root.mainloop()

# Copy all the other functions from index_old.py and:
# 1. Make them methods of ScoreKeeperUI class
# 2. Replace global variables with self.
# 3. Replace direct access to frames/listboxes with self.
# 4. Update function calls to use self.
# ...rest of the UI methods...
