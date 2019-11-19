"""Statistics module containing basic stats related functions"""


def predict_value(x, slope, y_int):
    """
    Predicts the value y depending on the equation of the line of best fit.
        y = mx + c, where m = slope, c = y intersect(value of y when x is 0)

    :param x: x value on line of best fit
    :type x: float
    :param slope: Slope of line of best fit.
    :type slope: float
    :param y_int: 
    """

    return x * slope + y_int


def get_y_intercept(x_list, y_list, slope=None):
    """
    Calculates the value of the y intercept.

    :param x_list: list of x values
    :type x_list: list
    :param: y_list: list of y values
    :type y_list: list
    :param slope: Slope of the line of best fit.
    :type slope: float
    :return: y intercept
    :rtype: float
    """

    if not slope and slope != 0:
        slope = get_slope(x_list, y_list)

    sum_y = sum(y_list)
    sum_x = sum(x_list)

    return (sum_y - slope * sum_x) / float(len(x_list))


def get_slope(x_list, y_list):
    """
    Gets the slope for line of best fit.

    :param x_list: list of x values
    :type x_list: list
    :param y_list: list of y values
    :return: slope of line
    :rtype: float
    """

    # Ensure each value is a float. Saves the need to do so later.
    x_list = [float(x) for x in x_list]
    y_list = [float(y) for y in y_list]

    x_sqr = [x ** 2 for x in x_list]

    xy = [x * y for x, y in zip(x_list, y_list)]

    sum_x = sum(x_list)
    sum_y = sum(y_list)
    sum_x_sqr = sum(x_sqr)
    sum_xy = sum(xy)
    # Sub each value into the equation for slope
    return (len(x_list) * sum_xy - sum_x * sum_y) / (len(x_list) * sum_x_sqr - sum_x ** 2)


def calculate_least_squares_variables(independent, dependant):
    """
    Calculates slope and y intersect for line of best fit:
        y = mx + c, where m = slope, c = y intersect(value of y when x is 0)

    :param independent:
    :param dependant:
    :return: Slope and y intercept for line of best fit
    """

    m = round(get_slope(independent, dependant), 4)
    c = round(get_y_intercept(independent, dependant, slope=m), 4)
    print('Line of best fit => y = {m}x + {c}'.format(m=m, c=c))
    return m, c


def get_cords_for_best_fit_line(x_data, y_data):
    """
    Gets two points on the line of best fit so it can be plotted.
    
    :param x_data: list of x axis values
    :type x_data: list
    :param y_data: list of y axis values
    :type y_data: list
    :return: Two points(min, max) on the line of best fit.
    :rtype: tuple of tuples
    """

    slope, c = calculate_least_squares_variables(x_data, y_data)
    min_x = min(x_data)
    max_x = max(x_data)
    cord_1 = (min_x, predict_value(min_x, slope=slope, y_int=c))
    cord_2 = (max_x, predict_value(max_x, slope=slope, y_int=c))

    return cord_1, cord_2
