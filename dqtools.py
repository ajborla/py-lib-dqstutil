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
    Given `s`, returns True if it is possibly a numeric-convertible string,
    such as a currency value or comma-separted numeric, or a suffixed
    value (such as a measurement). Note that version strings (often having
    two or more decimal points) are NOT considered possible numerics.

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
    """
    Given `s`, returns string indicating its possible type, one of:

        T  - text
        N  - numeric (safely convertible to)
        PD - possibly a date
        PN - possibly a numeric

    :param s: str
    :return: str

    >>> determine_column_type('sgsgsg')
    'T'

    >>> determine_column_type('15M')
    'PN'

    >>> determine_column_type('-4.1')
    'N'

    >>> determine_column_type('January 1, 1999')
    'PD'
    """
    if is_numeric(s): return 'N'
    if is_possible_numeric(s): return 'PN'
    if is_possible_date(s): return 'PD'
    return 'T'

def inspect_dataset(dataset, header, generate_report=True):
    """
    Given `dataset` and `header`, inspects `dataset` collecting
    metadata, and either returns metadata or generates, and
    prints, a report.

    `dataset` is a list of lists, each sublist a 'row' in the
    dataset, `header` is a list of strings, each identifying a
    corresponding 'column' in the dataset. The metadata collected
    includes:
        rowskip, a list of non length-conformant row numbers
        columns, a dict, keyed by column name, each containing a
          dict of column-type-identifying codes (see the function,
          'determine_column_type' for details)
        uniques, a dict, keyed by column name, each containing the
          count of unique values in text-only-type columns
        duplicates, a dict, keyed by column name, each containing the
          count of duplicate values in text-only-type columns

    :param dataset: list
    :param header: list
    :param generate_report: bool

    :return: None|tuple(list,dict,dict,dict)

    >>> header = ['a', 'b', 'c']
    >>> dataset = [['a1', 'b1', 'c1'],['a2', 'c2'],['a3', 'b3', 'c3'], ['a4', 'bib', '3'], ['ay', 'bib', 'x'], ['ay', 'bib', 'x']]
    >>> rowskip, columns, uniques, duplicates = inspect_dataset(dataset, header, generate_report=False)
    >>> rowskip, columns, uniques, duplicates
    ([1], {'a': {'PN': 3, 'T': 2}, 'b': {'PN': 2, 'T': 3}, 'c': {'PN': 2, 'N': 1, 'T': 2}}, {'a': 1, 'b': 1, 'c': 1}, {'a': 1, 'b': 2, 'c': 1})

    >>> header = ['a', 'b', 'c']
    >>> dataset = [['a1', 'b1', 'c1'],['a2', 'c2'],['a3', 'b3', 'c3'], ['a4', 'bib', '3'], ['ay', 'bib', 'x'], ['ay', 'bib', 'x']]
    >>> inspect_dataset(dataset, header, generate_report=True)
    Invalid (incorrect length) row numbers:[1]
    <BLANKLINE>
    Tentative column type(s) [T - text, N - numeric, PN - possible numeric, PD - possible date]:
    <BLANKLINE>
    {'a': {'PN': 3, 'T': 2}, 'b': {'PN': 2, 'T': 3}, 'c': {'PN': 2, 'N': 1, 'T': 2}}
    <BLANKLINE>
    Unique value counts (non-numeric and non-date columns only):
    <BLANKLINE>
    {'a': 1, 'b': 1, 'c': 1}
    <BLANKLINE>
    Duplicate value counts (non-numeric and non-date columns only):
    <BLANKLINE>
    {'a': 1, 'b': 2, 'c': 1}
    """
    # Column metadata repository keyed using column headers
    columns = {}
    for colname in header:
        columns[colname] = {}
    # Collect non length-conformant row numbers
    rowskip = []
    rowlen = len(header)
    for r, row in enumerate(dataset):
        # Check for row length conformance
        if len(row) != rowlen:
            rowskip.append(r)
    # Collect column type data
    for r, row in enumerate(dataset):
        # Skip non length-conformant rows
        if r in rowskip: continue
        # Check column type conformance
        for colname, colval in zip(header, row):
            coltype = determine_column_type(colval)
            if coltype in columns[colname]:
                columns[colname][coltype] += 1
            else:
                columns[colname][coltype] = 1
    # Collect unique value data
    uniques, duplicates = {}, {}
    for colname in header:
        uniques[colname] = []
        duplicates[colname] = []
    for r, row in enumerate(dataset):
        # Skip non length-conformant rows
        if r in rowskip: continue
        # Collect unique values for non-date and non-numeric columns
        for colname, colval in zip(header, row):
            # Check both the column type and the current value
            if 'T' not in columns[colname]: continue
            if determine_column_type(colval) != 'T': continue
            if colval not in uniques[colname]:
                uniques[colname].append(colval)
            else:
                duplicates[colname].append(colval)
    # Replace collect unique values with their count
    for colname in header:
        uqcollen = len(uniques[colname])
        ducollen = len(duplicates[colname])
        # Remove entries with zero unique count
        if uqcollen < 1:
            del uniques[colname]
            del duplicates[colname]
        else:
            uniques[colname] = uqcollen
            duplicates[colname] = ducollen
    # Generate report if requested
    if generate_report:
        print('Invalid (incorrect length) row numbers:', end='')
        print(rowskip)
        print('\nTentative column type(s) [T - text, N - numeric, PN - possible numeric, PD - possible date]:\n')
        print(columns)
        print('\nUnique value counts (non-numeric and non-date columns only):\n')
        print(uniques)
        print('\nDuplicate value counts (non-numeric and non-date columns only):\n')
        print(duplicates)
    else:
        # Return collected metadata as tuple
        return rowskip, columns, uniques, duplicates,

def extract_unique_values(values):
    """
    Given a list, `values`, the unique values are returned as a list.

    :param values: list
    :return: list

    >>> values = ['a', 't', 'z', 'k', 'v', 'z', 't']
    >>> uniques = ['a', 't', 'z', 'k', 'v']
    >>> extract_unique_values(values) == uniques
    True

    >>> values = [1, 2, 3, 1]
    >>> uniques = [1, 2, 3]
    >>> extract_unique_values(values) == uniques
    True
    """
    pass

if __name__ == "__main__":
    doctest.testmod()

