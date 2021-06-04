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
    False

def is_possible_numeric(s):
    False

def determine_column_type(s):
    pass

def inspect_dataset(dataset, header, generate_report=True):
    pass

if __name__ == "__main__":
    doctest.testmod()

