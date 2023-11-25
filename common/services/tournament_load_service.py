import json
from django.conf import settings
from django.contrib import messages

from common.services.lichess_api_service import lichess_api_service
from game.models import Game
from tournament.models import (
    Player,
    Team,
    TournamentPlayerResult,
    TournamentTeamResult,
    Tournament,
)


class TournamentLoadService:
    def _get_tournament_data(self, tournament_id):
        if settings.MOCK_RESPONSES:
            f = open('/Users/givanov/PycharmProjects/bnl/bnl/response_examples/tournament_results.json')
            line = f.readline()
            return json.loads(line)
        success, data = lichess_api_service.get_tournament_data(tournament_id)
        if not success:
            return {}

        return data

    def process_team_data(self, team_data, tournament):
        team, _ = Team.objects.get_or_create(lichess_id=team_data['id'], defaults={'name': team_data['id']})
        team_result, _ = TournamentTeamResult.objects.get_or_create(
            team=team,
            tournament=tournament,
            defaults={'score': team_data['score'], 'rank': team_data['rank']}
        )

    def process_player_data(self, player_data_set, tournament):

        player, _ = Player.objects.get_or_create(
            lichess_id=player_data_set['name'], defaults={'username': player_data_set['name']}
        )
        player_result, _ = TournamentPlayerResult.objects.get_or_create(
            player=player,
            tournament=tournament,
            defaults={'score': player_data_set['score'], 'rank': player_data_set['rank']}
        )

    def process_games(self, tournament):
        success, response = lichess_api_service.get_tournament_games(tournament.lichess_id)
        games_to_save = []
        for game in games:
            new_game = Game(
                player_white=Player.objects.get(lichess_id=game['players']['white']['userId']),
                player_black=Player.objects.get(lichess_id=game['players']['black']['userId']),
                tournament=tournament,
                result=game['status'],
                opening=game['opening']['name'],
            )
            games_to_save.append(new_game)
        Game.objects.bulk_create(games_to_save)

    def process_tournament(self, tournament):
        data = self._get_tournament_data(tournament.lichess_id)
        tournament.name = data['fullName']
        for team_data in data['teamStanding']:
            self.process_team_data(team_data, tournament)
        for i in range(50):
            data = self._get_tournament_data(tournament.lichess_id + '?page=' + str(i))
            for player_data_set in data['standing']['players']:
                self.process_player_data(player_data_set, tournament)
        #self.process_games(tournament)
        tournament.save()

    def load_season_tournaments(self, season):
        success, response = lichess_api_service.get_user_tournaments()
        if not success:
            return False, response
        for line in response.text.split('\n'):
            tournament_data = json.loads(line)
            if season.name:
                tournament, _ = Tournament.objects.get_or_create(
                    lichess_id=tournament_data['id'],
                    defaults={
                        'name': tournament_data['fullName'],
                        'season': season,
                    }
                )
                self.process_tournament(tournament)
        return True, {}

tournament_load_service = TournamentLoadService()