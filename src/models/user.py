from dataclasses import dataclass


@dataclass
class User:
    id: int
    user_name: str
    display_name: str
    team: str = None

    def add_team(self, team):
        self.team = team
