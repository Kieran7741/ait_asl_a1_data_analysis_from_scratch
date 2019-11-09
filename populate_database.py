import os
from tabulate import tabulate
import sqlite3


fifa_dataset = './dataset/fifa20_data.csv'


def process_row_string(row):
    """Due to some strange formatting of positions we need to carry out some steps"""
    split_row = row.replace('"', '').split(',')
    positions = []
    position_start_index = 3
    position_end_index = position_start_index

    for pos in split_row[position_start_index:]:
        try:
            int(pos)
            break
        except ValueError:
            positions.append(pos)
            position_end_index += 1

    positions = ';'.join(positions)

    return split_row[:position_start_index] + [positions] + split_row[position_end_index:]


def remove_spaces_from_headers(headers):

    new_headers = []
    for header in headers:
        header = header.replace(' ', '_')
        new_headers.append(header)

    return new_headers


def load_csv(csv_file_path):
    """
    Loads the dataset csv file. One issue with the data set: position is multiple positions comma separated
    :param csv_file_path:
    :return: Dataset headers and rows
    :rtype: tuple
    """
    data_rows = []

    if os.path.exists(csv_file_path):
        print('File exists: {0}'.format(csv_file_path))
        with open(csv_file_path, 'r') as csv:
            # First line of the csv contains the headers
            # Need to also remove the space and '/' in any of the headers. This makes it easier to create the SQL player table.
            headers = [header.replace(' ', '_').replace('/', '_') for header in csv.readline().strip('\n').split(',')]

            for line in csv.readlines():
                data_rows.append(process_row_string(line.strip('\n')))

            return headers, data_rows

    print('File does not exists: {0}'.format(csv_file_path))


def determine_sql_type(value):
    """
    Determine the SQL type of the value. Numbers can be float or int
    :param value: Target value to determine sql type.
    :type value: str
    :return: sql type
    :rtype: str
    """

    if value.isdigit():
        return 'int'
    else:
        try:
            float(value)
            return 'real'
        except ValueError:
            return 'text'


def print_tabulated_csv(csv_file_path, num_rows=10):
    """
    Prints tabulated view of the csv file.
    :param csv_file_path: Path to csv file.
    :type csv_file_path: str
    :param num_rows: Number of rows to display.
    :type num_rows: int
    """

    headers, rows = load_csv(csv_file_path)
    print(tabulate(rows[:num_rows], headers=headers))


def create_players_table(csv_file_path):
    """
    create fifa dataset to a sqllite db
    :param csv_file_path: File path to dataset
    :type csv_file_path: str
    """
    headers, rows = load_csv(csv_file_path)

    value_type_pairs = ['{name} {sql_type}'.format(name=value_name, sql_type=determine_sql_type(value))
                        for value_name, value in zip(headers, rows[0])]

    connection = sqlite3.connect('players.db')
    connection.execute('CREATE TABLE IF NOT EXISTS players({value_type_pairs})'.format(value_type_pairs=','.join(value_type_pairs)))
    connection.commit()
    connection.close()

    populate_players_table(rows)


def populate_players_table(players):
    """
    Insert players into db
    :param players: list of players
    """

    connection = sqlite3.connect('players.db')

    print(['?'] * (len(players[0])))
    print(len(players[0]))
    print(tuple(players[0]))

    insert_query = 'INSERT INTO players VALUES({0})'.format(','.join(['?']*(len(players[0]))))
    print(insert_query)

    for player in players:
        connection.execute(insert_query, tuple(player))
    connection.commit()
    connection.close()


if __name__ == '__main__':
    """Run this file as script"""

    print_tabulated_csv(fifa_dataset)
