import pandas as pd
import json

from fatcories.common import SMALL_POINTS_MAP,PLAYER_POINTS_MAP, TEAM_POINTS_MAP

penalty_points = {
    'FantasticInspiration' : 64
}

def calculate_total_points(group):
    total_points = sum(PLAYER_POINTS_MAP.get(place, 0) for place in group['rank']) - penalty_points.get(group['username'].values[0], 0)
    return pd.Series({'total_points': total_points, 'team': group['name'].values[0]})

def calculate_total_points_sub(group):
    total_points = sum(SMALL_POINTS_MAP.get(place, 0) for place in group['place'])
    return pd.Series({'total_points': total_points, 'team': group['name'].values[0]})

def calculate_total_team_points(group):
    total_points = sum(TEAM_POINTS_MAP.get(place, 0) for place in group['rank'])
    return pd.Series({'total_points': total_points})

def make_dict_from_raw_data(raw_data):
    result = []
    for row in raw_data:
        record = row['fields']
        record['id'] = row['pk']
        result.append(record)
    return result


tournament_info_raw = json.load(open('data/tournament.json'))
team_info_raw = json.load(open('data/team.json'))
player_info_raw = json.load(open('data/player.json'))
tournament_results_raw = json.load(open('data/TournamentTeamResult.json'))
player_results_raw = json.load(open('data/TournamentPlayerResult.json'))

tournament_info = make_dict_from_raw_data(tournament_info_raw)
team_info = make_dict_from_raw_data(team_info_raw)
player_info = make_dict_from_raw_data(player_info_raw)
tournament_results = make_dict_from_raw_data(tournament_results_raw)
player_results = make_dict_from_raw_data(player_results_raw)

tournament_df = pd.DataFrame(tournament_info)
team_df = pd.DataFrame(team_info)
player_df = pd.DataFrame(player_info)
tournament_results_df = pd.DataFrame(tournament_results)
player_results_df = pd.DataFrame(player_results)

full_players_results_df = player_results_df.merge(player_df, left_on='player', right_on='id')
full_players_results_df = full_players_results_df.merge(team_df, left_on='team_y', right_on='id')
full_teams_results_df = tournament_results_df.merge(team_df, left_on='team', right_on='id')

young_players_result = full_players_results_df[full_players_results_df['is_youngster']].loc[:, ['username', 'tournament', 'score', 'rank', 'name']]
woman_players_result = full_players_results_df[full_players_results_df['is_woman']].loc[:, ['username', 'tournament', 'score', 'rank', 'name']]

young_players_result['place'] = young_players_result.groupby('tournament')['rank'].rank(method='dense')
woman_players_result['place'] = woman_players_result.groupby('tournament')['rank'].rank(method='dense')

player_season_points = full_players_results_df.groupby('username').apply(calculate_total_points).sort_values('total_points', ascending=False).reset_index()
team_season_points = full_teams_results_df.groupby('name').apply(calculate_total_team_points).sort_values('total_points', ascending=False).reset_index()
young_players_points = young_players_result.groupby('username').apply(calculate_total_points_sub).sort_values('total_points', ascending=False).reset_index()
woman_players_points = woman_players_result.groupby('username').apply(calculate_total_points_sub).sort_values('total_points', ascending=False).reset_index()

player_season_points.index = player_season_points.index + 1
team_season_points.index = team_season_points.index + 1
young_players_points.index = young_players_points.index + 1
woman_players_points.index = woman_players_points.index + 1

class PdStandingsService:
    def __init__(self, pd_standings_repository):
        self.pd_standings_repository = pd_standings_repository

    def get_standings(self):
        return self.pd_standings_repository.get_standings()

    def calculate_total_points(self, group):
        total_points = sum(PLAYER_POINTS_MAP.get(place, 0) for place in group['rank']) - penalty_points.get(
            group['username'].values[0], 0)
        return pd.Series({'total_points': total_points, 'team': group['name'].values[0]})

    def calculate_total_points_sub(self, group):
        total_points = sum(SMALL_POINTS_MAP.get(place, 0) for place in group['place'])
        return pd.Series({'total_points': total_points, 'team': group['name'].values[0]})

    def calculate_total_team_points(self, group):
        total_points = sum(TEAM_POINTS_MAP.get(place, 0) for place in group['rank'])
        return pd.Series({'total_points': total_points})

    def make_dict_from_raw_data(self, raw_data):
        result = []
        for row in raw_data:
            record = row['fields']
            record['id'] = row['pk']
            result.append(record)
        return result