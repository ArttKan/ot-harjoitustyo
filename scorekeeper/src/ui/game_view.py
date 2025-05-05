import tkinter as tk
from tkinter import messagebox
from entities.event import Event


class GameView:
    def __init__(self, root, score_service):
        """Initialize game view.

        Args:
            root: tkinter root window
            score_service: ScoreService instance for game logic
        """
        self._root = root
        self._score_service = score_service
        self._frame = None
        self._event_listbox = None
        self._score_label = None
        self._event_types = ["2-Pointer", "3-Pointer",
                             "Rebound", "Foul", "Technical Foul"]

        self._initialize()

    def _initialize(self):
        """Set up the game view layout."""
        self._frame = tk.Frame(self._root)

        game_info = tk.Frame(self._frame)
        game_info.grid(row=0, column=0, columnspan=3, pady=10)
        game_info.grid_columnconfigure(1, weight=1)

        team1, team2 = self._score_service.get_current_game().get_teams()

        tk.Label(game_info, text=team1.name, font=("Arial", 14, "bold")).grid(
            row=0, column=0, padx=20)

        self._score_label = tk.Label(
            game_info, text="0 - 0", font=("Arial", 14, "bold"))
        self._score_label.grid(row=0, column=1, padx=20)

        tk.Label(game_info, text=team2.name, font=("Arial", 14, "bold")).grid(
            row=0, column=2, padx=20)

        event_buttons = tk.Frame(self._frame)
        event_buttons.grid(row=1, column=0, columnspan=2, pady=10)

        for event_type in self._event_types:
            tk.Button(
                event_buttons,
                text=event_type,
                command=lambda t=event_type: self._handle_event_type_selection(
                    t)
            ).pack(side=tk.LEFT, padx=5)

        tk.Label(self._frame, text="Game Events:", font=("Arial", 12, "bold")).grid(
            row=3, column=0, columnspan=2, pady=(10, 0))

        self._event_listbox = tk.Listbox(self._frame, width=50, height=15)
        self._event_listbox.grid(row=4, column=0, columnspan=2, pady=10)

        self._frame.pack(pady=20)

    def _handle_event_type_selection(self, event_type):
        """Handle event type button click."""
        team1, team2 = self._score_service.get_current_game().get_teams()
        selection_window = tk.Toplevel(self._root)
        selection_window.title("Select Team")

        tk.Button(
            selection_window,
            text=team1.name,
            command=lambda: self._show_player_selection(
                selection_window, team1, event_type)
        ).pack(pady=5)

        tk.Button(
            selection_window,
            text=team2.name,
            command=lambda: self._show_player_selection(
                selection_window, team2, event_type)
        ).pack(pady=5)

    def _show_player_selection(self, parent_window, team, event_type):
        """Show player selection for the chosen team."""
        parent_window.destroy()
        selection_window = tk.Toplevel(self._root)
        selection_window.title("Select Player")

        listbox = tk.Listbox(selection_window, height=10)
        listbox.pack(pady=10)

        for player in team.get_players():
            listbox.insert(tk.END, f"#{player.number:02d} {player.name}")

        tk.Button(
            selection_window,
            text="Confirm",
            command=lambda: self._handle_event_creation(
                selection_window, event_type, team, listbox.curselection())
        ).pack(pady=5)

    def _show_event_confirmation(self, event_type, team, player):
        """Show event confirmation dialog."""
        dialog = tk.Toplevel(self._root)
        dialog.title("Confirm Event")

        tk.Label(dialog,
                 text=f"Event: {event_type}",
                 font=("Arial", 12, "bold")).pack(pady=5)
        tk.Label(dialog,
                 text=f"Team: {team.name}").pack(pady=5)
        tk.Label(dialog,
                 text=f"Player: #{player.number:02d} {player.name}").pack(pady=5)

        tk.Button(dialog,
                  text="Confirm",
                  command=lambda: self._confirm_event(
                      dialog, event_type, team, player)
                  ).pack(pady=10)

    def _handle_event_creation(self, window, event_type, team, selection):
        """Create and add new event."""
        if not selection:
            messagebox.showerror("Error", "Please select a player")
            return

        player = team.get_players()[selection[0]]
        window.destroy()
        self._show_event_confirmation(event_type, team, player)

    def _update_event_list(self):
        """Update the event list display."""
        if not self._event_listbox:
            return

        self._event_listbox.delete(0, tk.END)

        events = self._score_service.get_events()
        print(f"Displaying {len(events)} events")

        for event in events:
            event_text = f"{event.type} - {event.team.name}"
            if event.player:
                event_text += f" - {event.player}"

            self._event_listbox.insert(0, event_text)

        self._event_listbox.update()
        self._event_listbox.see(0)

    def _update_score_display(self):
        """Update the score display."""
        team1, team2 = self._score_service.get_current_game().get_teams()
        score1 = self._score_service.get_team_score(team1.name)
        score2 = self._score_service.get_team_score(team2.name)
        self._score_label.config(text=f"{score1} - {score2}")

    def _confirm_event(self, dialog, event_type, team, player):
        """Handle event confirmation.

        Args:
            dialog: Confirmation dialog window
            event_type: Type of event
            team: Team object
            player: Player object
        """
        event = Event(event_type, player, team)

        try:
            result = self._score_service.add_event(event)
            if result:
                print(
                    f"Event saved successfully: {event_type} by {player.name}")
                dialog.destroy()

                self._root.after(100, self._update_event_list)
                self._root.after(100, self._update_score_display)

                events = self._score_service.get_events()
                print(f"Current events in database: {len(events)}")
            else:
                print("Failed to save event")
                messagebox.showerror("Error", "Failed to save event")
        except Exception as error:
            print(f"Error during event confirmation: {error}")
            messagebox.showerror("Error", f"Error saving event: {str(error)}")

    def destroy(self):
        """Destroy this view."""
        self._frame.destroy()
