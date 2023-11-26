import csv

from django.contrib import admin, messages
from django.http import HttpResponse

from common.services.lichess_api_service import lichess_api_service
from common.services.score_report_service import ReportService
from common.services.tournament_load_service import tournament_load_service
from .models import Tournament, Team, Player, TournamentPlayerResult, TournamentTeamResult, Season


class TournamentAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'description', 'link')
    actions = ['update_data_from_lichess']

    def update_data_from_lichess(self,  request, queryset):
        for tournament in queryset:
            tournament_load_service.process_tournament(tournament)


class TeamAdmin(admin.ModelAdmin):
    actions = ['update_team_info']

    def update_team_info(self, request, queryset):
        for team in queryset:
            success, team_info = lichess_api_service.get_team_data(team.lichess_id)
            if not success:
                continue
            team.name = team_info['name']
            team.description = team_info['description']
            team.save()


class SeasonAdmin(admin.ModelAdmin):
    actions = ['get_team_standings', 'get_player_standings', 'get_young_player_standings', 'load_season_tournaments']

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

    def load_season_tournaments(self, request, queryset):
        if len(queryset) > 1:
            messages.error(request, 'Please select only one season')
            return
        season = queryset[0]
        tournament_load_service.load_season_tournaments(season)
        messages.success(request, 'Tournaments loaded successfully')

class PlayerAdmin(admin.ModelAdmin):
    search_fields = ['username']

class TournamentTeamResultAdmin(admin.ModelAdmin):
    list_display = ('tournament', 'team', 'rank', 'score')
    list_filter = ('tournament', 'team')

admin.site.register(Tournament, TournamentAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(TournamentPlayerResult)
admin.site.register(TournamentTeamResult, TournamentTeamResultAdmin)
admin.site.register(Season, SeasonAdmin)
