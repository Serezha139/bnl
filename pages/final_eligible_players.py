import streamlit as st
import pandas as pd
import json


st.set_page_config(
    page_title="Игроки, попадающие в финал",
    page_icon="♔",
)

st.title('Игроки, попадающие в финал')
st.text('''
СКОРО ТУТ ВСЕ ПОЯВИТСЯ


Для попадания в финал необходимо:
 - сыграть минимум в 6 турнирах
 - по 7 партий в каждом
 - набрать не менее 8 очков в каждом
''')


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
player_results_raw = json.load(open('data/TournamentPlayerResult.json'))

team_info = make_dict_from_raw_data(team_info_raw)
player_info = make_dict_from_raw_data(player_info_raw)
player_results = make_dict_from_raw_data(player_results_raw)

team_df = pd.DataFrame(team_info)
player_df = pd.DataFrame(player_info)
player_results_df = pd.DataFrame(player_results)

full_players_results_df = player_results_df.merge(player_df, left_on='player', right_on='id')
full_players_results_df = full_players_results_df.merge(team_df, left_on='team_y', right_on='id')

full_players_results_df = full_players_results_df[full_players_results_df['score'] >= 8, full_players_results_df['nb_games'] >= 7]
full_players_results_df = full_players_results_df.groupby('username').filter(lambda x: len(x) >= 6)
unique_players_with_teams = full_players_results_df.groupby('username')['name'].nunique()
full_players_results_df



