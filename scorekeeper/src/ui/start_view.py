import tkinter as tk
from tkinter import ttk


class StartView:
    def __init__(self, root, handle_start):
        """Initialize start view.

        Args:
            root: Tkinter root window
            handle_start: Callback for start button
        """
        self._root = root
        self._handle_start = handle_start
        self._frame = None
        self._initialize()

    def _initialize(self):
        """Set up the start view layout."""
        self._frame = ttk.Frame(self._root)

        title_label = ttk.Label(
            self._frame,
            text="Scorekeeper",
            font=("Arial", 24, "bold")
        )
        title_label.pack(pady=50)

        start_button = ttk.Button(
            self._frame,
            text="Start New Game",
            command=self._handle_start
        )
        start_button.pack(pady=20)

        self._frame.pack(expand=True)

    def destroy(self):
        """Destroy this view."""
        self._frame.destroy()
