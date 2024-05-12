class BaseTeamDAO:
    def __init__(self, db):
        self.db = db

    def get_team(self, team_id):
        raise NotImplementedError

    def create_team(self, team):
        raise NotImplementedError

    def update_team(self, team):
        raise NotImplementedError

    def delete_team(self, team_id):
        raise NotImplementedError