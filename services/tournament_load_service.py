import json
from django.conf import settings
from django.contrib import messages

from services.lichess_api_service import lichess_api_service
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
        success, data = lichess_api_service.get_tournament_data(tournament_id)
        if not success:
            return {}

        return data

    def ensure_team_exists(self, team_id, team_data: list,):
        team, _ = Team.objects.get_or_create(lichess_id=team_id, defaults={'name': team_data[0]})

    def process_team_data(self, team_data, tournament):
        team = Team.objects.get(lichess_id=team_data['id'])
        team_result, _ = TournamentTeamResult.objects.get_or_create(
            team=team,
            tournament=tournament,
            defaults={'score': team_data['score'], 'rank': team_data['rank']}
        )

    def process_player_data(self, player_data_set, tournament):

        player, _ = Player.objects.get_or_create(
            lichess_id=player_data_set['name'], defaults={
                'username': player_data_set['name'],
                'team': Team.objects.get(lichess_id=player_data_set['team']),
            }
        )
        player_result, _ = TournamentPlayerResult.objects.get_or_create(
            player=player,
            tournament=tournament,
            defaults={'score': player_data_set['score'], 'rank': player_data_set['rank']}
        )

    def process_games(self, tournament):
        success, games = lichess_api_service.get_tournament_games(tournament.lichess_id)
        for game in games:
            try:
                new_game, _ = Game.objects.get_or_create(
                    link=game.link,
                    defaults={
                        'player_white': Player.objects.get(lichess_id=game.player_white),
                        'player_black': Player.objects.get(lichess_id=game.player_black),
                        'tournament': tournament,
                        'result': game.result,
                        'opening': game.opening,
                    }
                )
            except Player.DoesNotExist:
                print(f'Player not found {game.player_white} or {game.player_black}')

    def process_tournament(self, tournament):
        data = self._get_tournament_data(tournament.lichess_id)
        tournament.name = data['fullName']
        for team_id, team_data in data['teamBattle']['teams'].items():
            self.ensure_team_exists(team_id, team_data)
        for team_data in data['teamStanding']:
            self.process_team_data(team_data, tournament)
        for i in range(50):
            data = self._get_tournament_data(tournament.lichess_id + '?page=' + str(i))
            for player_data_set in data['standing']['players']:
                self.process_player_data(player_data_set, tournament)
        tournament.save()

    def load_season_tournaments(self, season):
        success, response = lichess_api_service.get_league_tournaments()
        if not success:
            return False, response
        season_start_date = season.start_date.timestamp()
        for line in response.text.split('\n'):
            tournament_data = json.loads(line)
            if season_start_date < tournament_data['startsAt']:
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