import requests
import datetime


class TournamentService:
    def __init__(self, tournament):
        self.tournament = tournament

    def update_data_from_lichess(self):
        base_url = f"https://lichess.org/api/tournament/{self.tournament.lichess_id}"
        response = requests.get(base_url)
        if response.status_code == 200:
            data = response.json()
            self.tournament.name = data['fullName']
            self.tournament.date = datetime.datetime.strptime(data['startsAt'], '%Y-%m-%dT%H:%M:%SZ')
            self.tournament.link = base_url
            self.tournament.save()
