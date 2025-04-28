import tkinter as tk
from services.score_service import ScoreService
from ui.start_view import StartView
from ui.team_selection_view import TeamSelectionView
from ui.player_view import PlayerView
from ui.game_view import GameView


class UI:
    def __init__(self, root):
        self._root = root
        self._current_view = None
        self._score_service = ScoreService()

    def start(self):
        """Start the UI with the initial view."""
        self._show_start_view()

    def _hide_current_view(self):
        """Hide the current view if it exists."""
        if self._current_view:
            self._current_view.destroy()

    def _show_start_view(self):
        """Show the start game view."""
        self._hide_current_view()
        self._current_view = StartView(
            self._root,
            self._show_team_selection_view
        )

    def _show_team_selection_view(self):
        """Show the team selection view."""
        self._hide_current_view()
        self._current_view = TeamSelectionView(
            self._root,
            self._score_service,
            self._show_player_view
        )

    def _show_player_view(self):
        """Show the player management view."""
        self._hide_current_view()
        self._current_view = PlayerView(
            self._root,
            self._score_service,
            self._show_game_view
        )

    def _show_game_view(self):
        """Show the game view."""
        self._hide_current_view()
        self._current_view = GameView(
            self._root,
            self._score_service
        )
