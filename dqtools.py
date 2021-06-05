import doctest

def is_numeric(s):
    """
    Given `s`, returns True if it is either a numeric type, or a numeric-convertible string.

    :param s: str
    :return: bool

    >>> is_numeric('sgsgsg')
    False

    >>> is_numeric([4,5,7])
    False

    >>> is_numeric({'a':5})
    False

    >>> is_numeric('6')
    True

    >>> is_numeric(6)
    True

    >>> is_numeric('4.1')
    True

    >>> is_numeric(4.1)
    True

    >>> is_numeric('-4.1')
    True

    >>> is_numeric(-4.1)
    True

    >>> is_numeric('4.1.4')
    False

    >>> is_numeric('56M')
    False

    >>> is_numeric(complex(3,4))
    True
    """
    def to_complex():
        try:
            complex(s)
            return True
        except:
            return False

    if type(s) is not str:
        return type(s) is int or type(s) is float or type(s) is complex
    else:
        return s.isnumeric() or to_complex()

def is_possible_date(s):
    """
    Given `s`, returns True if it is possibly a date-convertible string.

    :param s: str
    :return: bool

    >>> is_possible_date('sgsgsg')
    False

    >>> is_possible_date('1/1/1')
    True

    >>> is_possible_date('1/1/1/')
    False

    >>> is_possible_date('1-1-1')
    True

    >>> is_possible_date('1--1-1')
    False

    >>> is_possible_date('January 1, 1999')
    True
    """
    s = s.lower()
    month_prefixes = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul',
                      'aug', 'sep', 'oct', 'nov', 'dec']
    return any(map(lambda m: m in s, month_prefixes)) or \
           len(list(filter(lambda c: c == '/' or c == '-', s))) == 2

def is_possible_numeric(s):
    """
    Given `s`, returns True if it possibly a numeric-convertible string.

    :param s: str
    :return: bool

    >>> is_possible_numeric('sgsgsg')
    False

    >>> is_possible_numeric('1/1/1')
    False

    >>> is_possible_numeric('January 1, 1999')
    False

    >>> is_possible_numeric('15M')
    True

    >>> is_possible_numeric('$14.34')
    True

    >>> is_possible_numeric('$$59')
    False

    >>> is_possible_numeric('1,456,234')
    True

    >>> is_possible_numeric('1.0.23')
    False

    >>> is_possible_numeric('1.23')
    True

    >>> is_possible_numeric('1,7kM')
    True
    """
    # Tests to determine whether `s` may be a possible numeric string
    contains_digits = any(map(lambda c: c.isdigit(), s))
    contains_zero_or_one_decimal_point = len(list(filter(lambda c: c == '.', s))) < 2
    contains_zero_or_one_dollar_sign = len(list(filter(lambda c: c == '$', s))) < 2
    is_not_possible_date = not is_possible_date(s)
    # Apply tests and return result
    status = contains_digits and is_not_possible_date and \
             contains_zero_or_one_decimal_point and contains_zero_or_one_dollar_sign
    return status

def determine_column_type(s):
    pass

def inspect_dataset(dataset, header, generate_report=True):
    pass

if __name__ == "__main__":
    doctest.testmod()

