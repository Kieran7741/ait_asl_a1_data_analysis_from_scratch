from sqlite3 import connect
import os


def create_dict_from_db_query(db_result, col_names):
    """
    Converts a list of tuples into a dict where each column name is the key.

        Example:
            [('David De Gea Quintana', '€205K'), ('Paul Pogba', '€250K')] -->
            {'Name': ['David De Gea Quintana', 'Paul Pogba'], 'Wage': ['€205K', '€250K']}

    :param db_result: Select query result
    :param col_names:
    :type col_names: list
    :return:
    """

    col_dict = {key: [] for key in col_names}
    for result in db_result:
        for key in col_names:
            # print(col_names.index(key))
            col_dict[key].append(result[col_names.index(key)])

    return col_dict


class DB:

    """Database object to interact with an existing SQL Lite database"""

    def __init__(self, db_path):
        """
        init method
        :param db_path: path to .db file containing the database
        :type db_path: str
        raises EnviornmentError: if .db does not exist
        """
        if not os.path.exists(db_path):
            raise EnvironmentError(f'Could not find db at provided path: {db_path}')

        self.connection = connect(db_path)
        self.table = db_path.split('/')[-1].split('.db')[0]
        self.result = [] # The most recent result from a db query.

    def select(self, select, where='', dict_result=True):
        """
        Execute SELECT queries.
        :param select: List of columns to select
        :type select: list
        :param where: Where clause for select query
        :type where: str
        :return: Result from select query
        :rtype: list of tuples
        """
        
        query = 'SELECT {select} FROM {_from}'.format(select=','.join(select), _from=self.table)
        if where:
            query += (f' WHERE {where}')
        print(query)
        if dict_result:
            self.result = create_dict_from_db_query(self.connection.execute(query).fetchall(), select)
            return self.result
        else:
            self.result = self.connection.execute(query).fetchall()
            return self.result 


if __name__ == '__main__':
    player_db = DB('players.db')
    print(player_db.select(['Name'], where='Club="Arsenal"'))