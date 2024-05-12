class BasePlayerDAO:
    def __init__(self, db):
        self.db = db

    def get_player(self, player_id):
        raise NotImplementedError

    def get_all_players(self):
        raise NotImplementedError

    def create_player(self, player):
        raise NotImplementedError

    def update_player(self, player):
        raise NotImplementedError

    def delete_player(self, player_id):
        raise NotImplementedError