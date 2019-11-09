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
    Loads the dataset csv file. One issue with the data set: position is multiple positions comma seperated
    :param csv_file_path:
    :return: Dataset headers and rows
    :rtype: tuple
    """
    data_rows = []

    if os.path.exists(csv_file_path):
        print('File exists: {0}'.format(csv_file_path))
        with open(csv_file_path, 'r') as csv:
            headers = csv.readline().strip('\n').split(',')
            for line in csv.readlines()[:20]:
                data_rows.append(process_row_string(line.strip('\n')))

            return headers, data_rows

    print('File does not exists: {0}'.format(csv_file_path))


header, rows = load_csv('./dataset/fifa20_data.csv')
print(tabulate(rows, headers=header))





