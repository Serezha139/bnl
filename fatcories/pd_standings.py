class PdStandingsService:
    def __init__(self, pd_standings_repository):
        self.pd_standings_repository = pd_standings_repository

    def get_standings(self):
        return self.pd_standings_repository.get_standings()

    tournament_df = pd.DataFrame(tournament_info)
    team_df = pd.DataFrame(team_info)
    player_df = pd.DataFrame(player_info)
    tournament_results_df = pd.DataFrame(tournament_results)
    player_results_df = pd.DataFrame(player_results)