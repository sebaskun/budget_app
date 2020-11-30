import math


def ceiling(x, y):
    """
    Returns number rounded up, away from zero, to the nearest multiple
    of significance. For example, if you want to avoid using pennies in
    your prices and your product is priced at $4.42, use the formula
    ceiling(4.42,0.05) to round prices up to the nearest nickel.
    """
    return y * math.ceil(x/y)
