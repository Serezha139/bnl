from tournament.models import Season
from fatcories.common import PLAYER_POINTS_MAP, TEAM_POINTS_MAP, SMALL_POINTS_MAP


class PlainStandingsService:

    def generate_player_standings_for_season(self, season):
        player_points = {}
        for tournament in season.tournament_set.all():
            for player_result in tournament.tournamentplayerresult_set.all():
                player = player_result.player
                player_points[player.username] = (
                        player_points.get(player.username, 0) +
                        PLAYER_POINTS_MAP.get(player_result.rank, 0)
                )
        sorted_results = sorted(player_points.items(), key=lambda x:x[1], reverse=True)
        return sorted_results

    def generate_team_standings_for_season(self, season):
        team_points = {}
        for tournament in season.tournament_set.all():
            for team_result in tournament.tournamentteamresult_set.all():
                team = team_result.team
                team_points[team.name] = team_points.get(team.name, 0) + TEAM_POINTS_MAP.get(team_result.rank, 0)
        sorted_results = sorted(team_points.items(), key=lambda x: x[1], reverse=True)
        return sorted_results

    def generate_team_standings_for_current_season(self):
        season = Season.objects.filter(is_current=True).first()
        return self.generate_team_standings_for_season(season)

    def generate_player_standings_for_current_season(self):
        season = Season.objects.filter(is_current=True).first()
        return self.generate_player_standings_for_season(season)

    def generate_youngster_standings_for_current_season(self):
        season = Season.objects.filter(is_current=True).first()
        return self.generate_youngster_standings_for_season(season)

    def generate_woman_standings_for_current_season(self):
        season = Season.objects.filter(is_current=True).first()
        return self.generate_women_standings_for_season(season)

    def generate_youngster_standings_for_season(self, season):
        player_points = {}
        for tournament in season.tournament_set.all():
            players_ranks = {}
            for player_result in tournament.tournamentplayerresult_set.all():
                player = player_result.player
                if not player.is_youngster:
                    continue
                players_ranks[player.username] = player_result.rank
            sorted_results = sorted(players_ranks.items(), key=lambda x: x[1])
            for i, (player, rank) in enumerate(sorted_results):
                player_points[player] = player_points.get(player, 0) + SMALL_POINTS_MAP.get(i + 1, 0)

        return sorted(player_points.items(), key=lambda x: x[1], reverse=True)

    def generate_women_standings_for_season(self, season):
        player_points = {}

        for tournament in season.tournament_set.all():
            players_ranks = {}
            for player_result in tournament.tournamentplayerresult_set.all():
                player = player_result.player
                if not player.is_woman:
                    continue
                players_ranks[player.username] = player_result.rank
            sorted_results = sorted(players_ranks.items(), key=lambda x: x[1])
            for i, (player, rank) in enumerate(sorted_results):
                player_points[player] = player_points.get(player, 0) + SMALL_POINTS_MAP.get(i + 1, 0)

        return sorted(player_points.items(), key=lambda x: x[1], reverse=True)
