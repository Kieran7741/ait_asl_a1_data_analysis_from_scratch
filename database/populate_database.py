"""
Script to Generate SQL Lite db from the Fifa_20 csv file
"""

import os
from tabulate import tabulate
import sqlite3
from csv import reader


fifa_dataset = '../dataset/fifa20_data.csv'


def remove_quote_from_height(row, index):
    """
    Using the csv.reader causes the height column to contain a trailing ".
    :param row: row containing height
    :type row: list
    :param index: height position
    :type index: int
    :return: Updated row
    :rtype: list
    """

    height = row[index]
    row[index] = height.replace('"', '')
    return row


def load_csv(csv_file_path):
    """
    Loads the dataset csv file.
    :param csv_file_path:
    :return: Dataset headers and rows
    :rtype: tuple
    """
    data_rows = []

    if os.path.exists(csv_file_path):
        print('File exists: {0}'.format(csv_file_path))
        with open(csv_file_path, 'r') as csv_file:

            contents = reader(csv_file, delimiter=',')
            # First line of the csv contains the headers
            # Need to also remove the space and '/' in any of the headers.
            # This makes it easier to create the SQL player table.
            headers = [header.replace(' ', '_').replace('/', '_') for header in next(contents)]

            for row in contents:
                data_rows.append(remove_quote_from_height(row, index=headers.index('Height')))

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


def create_players_db(csv_file_path):
    """
    Convert fifa dataset to a sqllite db.
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

    insert_query = 'INSERT INTO players VALUES({0})'.format(','.join(['?']*(len(players[0]))))

    for player in players:
        connection.execute(insert_query, tuple(player))
    connection.commit()
    connection.close()


if __name__ == '__main__':
    """Run this file as script"""

    # Displays the CSV file in table format. If you are having issues viewing in the terminal it is due to line wrapping
    # Pipe the output to a file ensure that lines are not wrapped by the viewer/editor
    print_tabulated_csv(fifa_dataset, num_rows=50)

    # Generate the players.db
    # create_players_db(fifa_dataset)
