from sqlite3 import connect


class DB:

    def __init__(self, db_path):

        self.connection = connect(db_path)
        
if __name__ == '__main__':
    player_db = DB('players.db')