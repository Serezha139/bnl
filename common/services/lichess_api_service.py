import json
import requests

GET_TOURNAMENT = 'get_tournament'
GET_TOURNAMENTS = 'get_tournaments'
GET_TOURNAMENT_RESULTS = 'get_tournament_results'
GET_PLAYER_INFO = 'get_player_info'
GET_TEAM_INFO = 'get_team_info'
GET_TOURNAMENT_GAMES = 'get_tournament_games'

URL_MAP = {
    GET_TOURNAMENT: 'https://lichess.org/api/tournament/%s',
    GET_TOURNAMENTS: 'https://lichess.org/api/user/bel_league_admin/tournament/created',
    GET_TOURNAMENT_RESULTS: 'https://lichess.org/api/tournament/{tournament_id}/results',
    GET_PLAYER_INFO: 'https://lichess.org/api/user/{username}',
    GET_TEAM_INFO: 'https://lichess.org/api/team/%s',
    GET_TOURNAMENT_GAMES: 'https://lichess.org/api/tournament/%s/games?&opening=true&moves=false',
}


class LichessApiService:
    def get_user_tournaments(self):
        url = URL_MAP.get(GET_TOURNAMENTS)
        response = requests.get(url)
        if not response.status_code == 200:
            return False, {'error_status_code': response.status_code}

        return True, response
    @staticmethod
    def get_tournament_data(tournament_id):
        url = URL_MAP.get(GET_TOURNAMENT) % tournament_id
        response = requests.get(url)
        if not response.status_code == 200:
            return False, {'error_status_code': response.status_code}

        return True, response.json()

    def parse_games(self, games_text):
        games = []
        for line in games_text.split('\n'):
            if not line:
                games.app
            games.append(json.loads(line))
        return games

    def get_tournament_games(self, tournament_id):
        url = URL_MAP.get(GET_TOURNAMENT_GAMES) % tournament_id
        response = requests.get(url)
        if not response.status_code == 200:
            return False, {'error_status_code': response.status_code}
        games = self.parse_games(response.text)
        return True, response

    @staticmethod
    def get_team_data(team_id):
        url = URL_MAP.get(GET_TEAM_INFO) % team_id
        response = requests.get(url)
        if not response.status_code == 200:
            return False, {'error_status_code': response.status_code}

        return True, response.json()



lichess_api_service = LichessApiService()