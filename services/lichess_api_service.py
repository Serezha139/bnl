import io
from dataclasses import dataclass
import json
import requests
import chess.pgn

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
    GET_TOURNAMENT_GAMES: 'https://lichess.org/api/tournament/%s/games?&opening=true&moves=false&pgnInJson=true',
}

@dataclass
class GameDataclass:
    player_white: str
    player_black: str
    result: str
    opening: str
    link: str
    tournament: str



class LichessApiService:
    @staticmethod
    def get_league_tournaments():
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

    @staticmethod
    def parse_games(games_text):
        text_io = io.StringIO(games_text)
        games_to_return = []
        while game := chess.pgn.read_game(text_io):
            player_white = game.headers['White']
            player_black = game.headers['Black']
            result = game.headers['Result']
            opening = game.headers['Opening']
            link = game.headers['Site']
            tournament = game.headers['Event']
            games_to_return.append(GameDataclass(player_white, player_black, result, opening, link, tournament))

        return games_to_return

    def get_tournament_games(self, tournament_id):
        url = URL_MAP.get(GET_TOURNAMENT_GAMES) % tournament_id
        response = requests.get(url)
        if not response.status_code == 200:
            return False, {'error_status_code': response.status_code}
        games = self.parse_games(response.text)
        return True, games

    @staticmethod
    def get_team_data(team_id):
        url = URL_MAP.get(GET_TEAM_INFO) % team_id
        response = requests.get(url)
        if not response.status_code == 200:
            return False, {'error_status_code': response.status_code}

        return True, response.json()


lichess_api_service = LichessApiService()