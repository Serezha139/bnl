from dataclasses import fields, dataclass


@dataclass
class TournamentData:
    name: str
    lichess_id: str


@dataclass
class TeamData:
    lichess_id: str
    name: str = ''


