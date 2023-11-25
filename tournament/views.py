from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from common.services.score_report_service import ReportService

def standings(request):
    service = ReportService()
    results_player = service.generate_player_standings_for_current_season()
    results_team = service.generate_team_standings_for_current_season()
    results_young = service.generate_youngster_standings_for_current_season()
    return render(
        request,
        'standings.html',
        {'results_player': results_player, 'results_team': results_team, 'results_young': results_young}
    )