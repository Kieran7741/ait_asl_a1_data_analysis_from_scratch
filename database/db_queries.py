from sqlite3 import connect


def select_cols(db, select, _from, where=''):

    if not where:
        query = 'SELECT {select} FROM {_from}'.format(select=','.join(select), _from=_from)
    else:
        query = 'SELECT {select} FROM {_from} WHERE {where}'.format(select=','.join(select), _from=_from, where=where)

    with connect(db) as conn:
        return create_dict_from_db_query(conn.execute(query).fetchall(), select)


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




