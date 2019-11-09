import os
from tabulate import tabulate


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
            headers = csv.readline().strip('\n').split(',')
            for line in csv.readlines():
                data_rows.append(process_row_string(line.strip('\n')))

            return headers, data_rows

    print('File does not exists: {0}'.format(csv_file_path))


def write_player_to_db(player, headers):

    for attr, header in zip(player, headers):

        print(header, ':', attr, ';type: {}'.format(determine_sql_type(attr)[-1]))


def determine_sql_type(value):
    """
    Determine the SQL type of the value. Numbers can be float or int
    :param value: Target value to determine sql type.
    :type value: str
    :return: tuple containing converted python type and sql type: (123, 'int')
    :rtype: tuple
    """

    if value.isdigit():
        return int(value), 'int'
    else:
        try:
            value = float(value)
            return value, 'real'
        except ValueError:
            return value, 'text'


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


print_tabulated_csv('./dataset/fifa20_data.csv')



