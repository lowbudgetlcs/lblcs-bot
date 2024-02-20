from dataclasses import dataclass


@dataclass
class User:
    user_id: int
    user_name: str
    display_name: str
    team: str = None

    def add_team(self, team):
        self.team_id = team
