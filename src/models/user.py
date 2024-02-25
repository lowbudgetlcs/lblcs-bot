from dataclasses import dataclass


@dataclass
class User:
    user_id: int
    user_name: str
    display_name: str
    team_id: int = None

    def add_team(self, team):
        self.team_id = team
    def __str__(self):
        return f"Name: {self.display_name} Team: {self.team_id}"