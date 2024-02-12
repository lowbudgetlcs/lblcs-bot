from dataclasses import dataclass, asdict
import json


@dataclass
class Metadata:
    league: str
    teams: list[str]
    series_id: int = 0
    game: int = 0

    def serialize(self):
        return json.dumps(asdict(self))
