import requests

GET_TOURNAMENT = 'get_tournament'
GET_TOURNAMENTS = 'get_tournaments'
GET_TOURNAMENT_RESULTS = 'get_tournament_results'
GET_PLAYER_INFO = 'get_player_info'
GET_TEAM_INFO = 'get_team_info'

URL_MAP = {
    GET_TOURNAMENT: 'https://lichess.org/api/tournament/%s',
    GET_TOURNAMENTS: 'https://lichess.org/api/user/bel_league_admin/tournament/created',
    GET_TOURNAMENT_RESULTS: 'https://lichess.org/api/tournament/{tournament_id}/results',
    GET_PLAYER_INFO: 'https://lichess.org/api/user/{username}',
    GET_TEAM_INFO: 'https://lichess.org/api/team/%s',
}


class LichessApiService:
    @staticmethod
    def get_tournament_data(tournament_id):
        url = URL_MAP.get(GET_TOURNAMENT) % tournament_id
        response = requests.get(url)
        if not response.status_code == 200:
            return False, {'error_status_code': response.status_code}

        return True, response.json()

    @staticmethod
    def get_team_data(team_id):
        url = URL_MAP.get(GET_TEAM_INFO) % team_id
        response = requests.get(url)
        if not response.status_code == 200:
            return False, {'error_status_code': response.status_code}

        return True, response.json()



lichess_api_service = LichessApiService()