from dataclasses import dataclass, asdict
import json

@dataclass
class Metadata:
    league: str
    team1: str
    team2: str
    game: int = 0

    def serialize(self):
        return json.dumps(asdict(self))
