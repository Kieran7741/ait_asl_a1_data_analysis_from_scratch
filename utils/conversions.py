"""Module to handel various conversions"""


def convert_money_string(money_str):
    """
    Convert a wage of the form $200k to 200000
    :param money_str:
    :type money_str: str
    :return: Amount as float
    """
    try:
        if any([order in money_str.lower() for order in ['k', 'm']]):
            multiplier = 1000 if money_str[-1].lower() == 'k' else 10000000
            return float(money_str[1:-1]) * multiplier
        else:
            return float(money_str[1:])
    except ValueError as e:
        print(f'Invalid string amount passed: {money_str}')
        return 0


def convert_feet_to_cm(height):
    """
    Convert a height in the form 5'10 to cm
    :param height: Height in feet.
    :type height: str
    :return: Height in cm
    :rtype: float
    """

    foot_to_cm = 30.48
    inch_to_cm = 2.45

    feet, inches = height.split("'")
    return int(feet) * foot_to_cm + float(inches) * inch_to_cm


def convert_weight_to_kg(weight):
    """
    Convert weight in the form '150lbs to kg'
    :param weight: Weight in lbs
    :type weight: str
    :return: Weight in kg
    :rtype: float
    """

    pound_to_kg = 0.453592
    num_pounds = int(weight.split('lbs')[0])
    return round(num_pounds * pound_to_kg, 2)

