import pandas as pd

YONGSTER_POINTS_MAP = {
    1: 13,
    2: 10,
    3: 8,
    4: 6,
    5: 5,
    6: 4,
    7: 3,
    8: 2,
    9: 1,
}

PLAYER_POINTS_MAP = {
    1: 25,
    2: 22,
    3: 20,
    4: 18,
    5: 17,
    6: 16,
    7: 15,
    8: 14,
    9: 13,
    10: 12,
    11: 11,
    12: 10,
    13: 9,
    14: 8,
    15: 7,
    16: 6,
    17: 5,
    18: 4,
    19: 3,
    20: 2,
}

TEAM_POINTS_MAP = {
    1: 13,
    2: 10,
    3: 8,
    4: 7,
    5: 6,
    6: 5,
    7: 4,
    8: 3,
    9: 2,
    10: 1,
}


class ReportService:
    def generate_player_standings_for_season(self, season):
        player_points = {}
        for tournament in season.tournament_set.all():
            for player_result in tournament.tournamentplayerresult_set.all():
                player = player_result.player
                player_points[player.username] = player_points.get(player.username, 0) + PLAYER_POINTS_MAP.get(player_result.rank, 0)
        return player_points


    def generate_team_standings_for_season(self, season):
        team_points = {}
        for tournament in season.tournament_set.all():
            for team_result in tournament.tournamentteamresult_set.all():
                team = team_result.team
                team_points[team.name] = team_points.get(team.name, 0) + TEAM_POINTS_MAP.get(team_result.rank, 0)
        return team_points

    def generate_team_standings_for_current_season(self):
        pass

    def generate_player_standings_for_current_season(self):
        pass

    def generate_youngster_standings_for_season(self, season):
        player_points = {}

        for tournament in season.tournament_set.all():
            players_ranks = {}
            for player_result in tournament.tournamentplayerresult_set.all():
                player = player_result.player
                if not player.is_youngster:
                    continue
                players_ranks[player.username] = player_result.rank
            df = pd.DataFrame.from_dict(players_ranks, orient='index', columns=['rank'])
            df = df.sort_values(by=['rank'])
            for i in range(1, len(df) + 1):
                player_points[df.index[i - 1]] = player_points.get(df.index[i - 1], 0) + YONGSTER_POINTS_MAP.get(i, 0)

        return player_points
