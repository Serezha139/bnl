class BaseTeamResultDAO:
    def __init__(self, db):
        self.db = db

    def get_team_results(self, tournament_id):
        raise NotImplementedError

    def get_team_result(self, tournament_id, team_id):
        raise NotImplementedError

    def create_team_result(self, tournament_id, team_id, team_name, team_score):
        raise NotImplementedError

    def update_team_result(self, tournament_id, team_id, team_score):
        raise NotImplementedError

    def delete_team_result(self, tournament_id, team_id):
        raise NotImplementedError