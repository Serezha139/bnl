import csv
import json

from django.contrib import admin, messages
from django.conf import settings
from django.http import HttpResponse

from common.services.lichess_api_service import lichess_api_service
from common.services.score_report_service import ReportService
from .models import Tournament, Team, Player, TournamentPlayerResult, TournamentTeamResult, Season


class TournamentAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'description', 'link')
    actions = ['update_data_from_lichess']

    def _get_tournament_data(self, request, tournament_id):
        if settings.MOCK_RESPONSES:
            f = open('/Users/givanov/PycharmProjects/bnl/bnl/response_examples/tournament_results.json')
            line = f.readline()
            return json.loads(line)
        success, data = lichess_api_service.get_tournament_data(tournament_id)
        if not success:
            messages.error(
                request=request,
                message='Unsuccessful attemts to retreive tournament data' + data['status_code']
            )
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

    def process_tournament(self, request, tournament):
        data = self._get_tournament_data(request, tournament.lichess_id)
        tournament.name = data['fullName']
        for team_data in data['teamStanding']:
            self.process_team_data(team_data, tournament)
        for i in range(50):
            data = self._get_tournament_data(request, tournament.lichess_id + '?page=' + str(i))
            for player_data_set in data['standing']['players']:
                self.process_player_data(player_data_set, tournament)
        tournament.save()

    def update_data_from_lichess(self,  request, queryset):
        for tournament in queryset:
            self.process_tournament(request, tournament)


class TeamAdmin(admin.ModelAdmin):
    actions = ['update_team_info']

    def update_team_info(self, request, queryset):
        for team in queryset:
            team_info = lichess_api_service.get_team_data(team.lichess_id)[1]
            team.name = team_info['name']
            team.description = team_info['description']
            team.save()

class SeasonAdmin(admin.ModelAdmin):
    actions = ['get_team_standings', 'get_player_standings', 'get_young_player_standings']

    def get_team_standings(self, request, queryset):
        if len(queryset) > 1:
            messages.error(request, 'Please select only one season')
            return
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="standings.csv"'
        writer = csv.writer(response)
        season = queryset[0]
        report_service = ReportService()
        team_standings = report_service.generate_team_standings_for_season(season)
        for team, points in team_standings.items():
            writer.writerow([team, points])
        return response

    def get_player_standings(self, request, queryset):
        if len(queryset) > 1:
            messages.error(request, 'Please select only one season')
            return
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="player_standings.csv"'
        writer = csv.writer(response)
        season = queryset[0]
        report_service = ReportService()
        player_standings = report_service.generate_player_standings_for_season(season)
        for player in player_standings:
            writer.writerow([player['rank'], player['player'], player['score']])
        return response

    def get_young_player_standings(self, request, queryset):
        if len(queryset) > 1:
            messages.error(request, 'Please select only one season')
            return
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="young_player_standings.csv"'
        writer = csv.writer(response)
        season = queryset[0]
        report_service = ReportService()
        player_standings = report_service.generate_youngster_standings_for_season(season)
        for player in player_standings:
            writer.writerow([player['rank'], player['player'], player['score']])
        return response

class PlayerAdmin(admin.ModelAdmin):
    search_fields = ['username']

admin.site.register(Tournament, TournamentAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(TournamentPlayerResult)
admin.site.register(TournamentTeamResult)
admin.site.register(Season, SeasonAdmin)
