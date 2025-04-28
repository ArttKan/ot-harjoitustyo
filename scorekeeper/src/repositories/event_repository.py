class EventRepository:
    def __init__(self):
        self.events = []

    def add_event(self, event):
        """Add a new event to the repository."""
        self.events.append(event)
        return event

    def get_all_events(self):
        """Get all events."""
        return self.events

    def get_events_by_team(self, team_name):
        """Get all events for a specific team."""
        return [event for event in self.events if event.team.name == team_name]

    def get_events_by_player(self, player_number):
        """Get all events for a specific player."""
        return [event for event in self.events if event.player.number == player_number]

    def get_scoring_events_by_team(self, team_name):
        """Get all scoring events for a team."""
        return [event for event in self.events
                if event.team.name == team_name and
                (event.type == "2-Pointer" or event.type == "3-Pointer")]
