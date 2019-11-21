"""Statistics module containing basic stats related functions"""


###############
# Basic stats #
###############

def average(target_list):
    """
    Calculate average value in the target list
    :param target_list: list to calculate average of
    :type target_list: list
    :return: average value in the list
    :rtype: float
    """
    return sum(target_list) / len(target_list)


def median(target_list):
    """
    Calculate median value in the target list.

    :param target_list: list to calculate median of
    :type target_list: list
    :return: The 'middle value'
    :rtype: float or int
    """

    target_list.sort()
    index = (len(target_list) - 1) // 2

    if len(target_list) % 2:
        return target_list[index]
    else:
        return (target_list[index] + target_list[index + 1]) / 2.0


def mode(target_list):
    """
    Calculate mode of the target list.
    Limitations of this function:
        If the list has two modes it will return the first mode.
            mode([1,1,2,2]) --> 1

    :param target_list: list to calculate mode of
    :type target_list: list
    :return: float or int
    """

    return max(target_list, key=target_list.count)


######################################
# Line of best fit related functions #
######################################


def predict_value(x, slope, y_int):
    """
    Predicts the value y depending on the equation of the line of best fit.
        y = mx + c, where m = slope, c = y intersect(value of y when x is 0)

    :param x: x value on line of best fit
    :type x: float
    :param slope: Slope of line of best fit.
    :type slope: float
    :param y_int: y intersect(value of y when x is 0)
    :type y_int: float
    :return: preficted y value
    :rtype: float
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


def calculate_least_squares_variables(x_values, y_values):
    """
    Calculates slope and y intersect for line of best fit:
        y = mx + c, where m = slope, c = y intersect(value of y when x is 0)

    :param x_values: list of x values used to calculate line of best fit.
    :type x_values: list
    :param y_values: list of y values used to calculate line of best fit
    :type y_values: list
    :return: Slope and y intercept for line of best fit
    :rtype: tuple
    """

    m = round(get_slope(x_values, y_values), 4)
    c = round(get_y_intercept(x_values, y_values, slope=m), 4)
    print('Line of best fit => y = {m}x + {c}'.format(m=m, c=c))
    return m, c


def get_cords_for_best_fit_line(x_list, y_list):
    """
    Gets two points on the line of best fit so it can be plotted.

    :param x_list: list of x axis values
    :type x_list: list
    :param y_list: list of y axis values
    :type y_list: list
    :return: Two points(min, max) on the line of best fit.
    :rtype: tuple of tuples
    """

    slope, c = calculate_least_squares_variables(x_list, y_list)
    min_x = min(x_list)
    max_x = max(x_list)
    cord_1 = (min_x, predict_value(min_x, slope=slope, y_int=c))
    cord_2 = (max_x, predict_value(max_x, slope=slope, y_int=c))

    return cord_1, cord_2
