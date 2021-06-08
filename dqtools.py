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
    Given a list, `values`, a type-specific unique-value determination
    algorithm is selected, and applied, with the unique values returned
    as a list, optionally sorted in ascending order if `sort` is set.
    Optional, too, is `sep`, used as a separator where `values`'
    elements are multi-(non-list)-element lists (elements are
    concatenated to create the entity on which uniqueness is determined).

    Return list comprises the unique values in `values`, and in the case
    where elements were lists, these are the list-contained values. Refer
    to the tests for examples.

    :param values: list
    :param sort: bool
    :param sep: str
    :return: list

    >>> values = {'a': 4}
    >>> extract_unique_values(values) is None
    True

    >>> values = []
    >>> extract_unique_values(values) is None
    True

    >>> values = ['d', 4, {'a': 4}, [3,4,5]]
    >>> extract_unique_values(values) is None
    True

    >>> values = ['a', 't', 'z', 'k', 'v', 'z', 't']
    >>> uniques = ['a', 't', 'z', 'k', 'v']
    >>> extract_unique_values(values) == uniques
    True

    >>> values = [1, 3, 2, 1]
    >>> uniques = [1, 3, 2]
    >>> extract_unique_values(values) == uniques
    True

    >>> values = [1, 3, 2, 1]
    >>> uniques = [1, 3, 2]
    >>> extract_unique_values(values, sort=True) == sorted(uniques)
    True

    >>> values = [['a1'], ['b1'], ['c1'], ['a2'], ['b1'], ['c1'], ['a1'], ['b2'], ['c1']]
    >>> uniques = ['a1', 'b1', 'c1', 'a2', 'b2']
    >>> sorted(extract_unique_values(values)) == sorted(uniques)
    True

    >>> values = [[1], [2], [3], [1]]
    >>> uniques = [1, 2, 3]
    >>> extract_unique_values(values) == uniques
    True

    >>> values = [['a1', 'b1', 'c1'], ['a2', 'b2', 'c2'], ['a3', 'b3', 'c3'], ['a2', 'b2', 'c2']]
    >>> uniques = ['a1|b1|c1', 'a2|b2|c2', 'a3|b3|c3']
    >>> sorted(extract_unique_values(values)) == sorted(uniques)
    True

    >>> values = [['a1'], ['b1'], [], ['a2'], ['b1']]
    >>> extract_unique_values(values) is None
    True

    >>> values = [['a1'], ['b1'], 0, ['a2'], ['b1']]
    >>> extract_unique_values(values) is None
    True

    >>> values = [['a1', 'b1', 'c1'], [], ['a3', 'b3', 'c3'], ['a2', 'b2', 'c2']]
    >>> extract_unique_values(values) is None
    True

    >>> values = [['a1', 'b1', 'c1'], ['a2', 'c2'], ['a3', 'b3', 'c3'], ['a2', 'b2', 'c2']]
    >>> extract_unique_values(values) is None
    True

    >>> values = [['a1', 'b1', 'c1'], ['a2', 0, 'c2'], ['a3', 'b3', 'c3'], ['a2', 'b2', 'c2']]
    >>> extract_unique_values(values) is None
    True

    >>> values = [[11, 12, 13], [34, 0, 85], [11, 12, 13]]
    >>> uniques = ['11|12|13', '34|0|85']
    >>> sorted(extract_unique_values(values)) == sorted(uniques)
    True
    """
    # Exclude obvious non-candidates
    if type(values) is not list or len(values) < 1:
        return None
    # Ensure homogeneity of list elements
    elem_type = type(values[0])
    if not all(map(lambda v: type(v) is elem_type, values)):
        return None
    # Select algorithm based on element type: list or other
    if elem_type is list:
        elem_len = len(values[0])
        # Ensure all sublists are non-empty, have identical length,
        # and do not, themselves contain lists
        if elem_len == 0:
            return None
        contains_no_list = lambda v: all(map(lambda x: type(x) is not list, v))
        is_homogenous = lambda v, w: all(map(lambda x: type(x) is type(w), v))
        if not all(map(lambda v: len(v) == elem_len and \
                       contains_no_list(v) and is_homogenous(v, v[0]), values)):
            return None
        if elem_len > 1:
            # Unique values returned as string, concatenation of individual values
            to_str = lambda v: map(lambda x: str(x), v)
            uniques = [sep.join(to_str(v)) for v in set([tuple(v) for v in values])]
        else:
            # Unique values returned as original type
            uniques = [v[0] for v in set([tuple(v) for v in values])]
    else:
        # Non-list element type; unique values returned as original type
        uniques = [v for i, v in enumerate(values) if v not in values[:i]]
    # Sorted (ascending) unique value list, if requested
    return sorted(uniques) if sort else uniques

def gen_freq_table(dataset, header, colname, sort_by_value=False, reverse=False):
    """
    Given  a `dataset`, its `header`, a column name, `colname`, generates
    a frequency table keyed by `colname`, and including both the count and
    relative percentage as a tuple. Returned table is sorted by key, that
    is, by `colname`, ascending. The value of optional boolean arguments,
    `sort_by_value` and `reverse`, determine alternate ordering of the
    table entries.

    :param dataset: list
    :param header: list
    :param colname: str
    :param sort_by_value: bool
    :param reverse: bool

    :return: dict

    >>> header = ['a', 'b', 'c']
    >>> ds = [['a1', 'b1', 'c1'],['a2', 'b2', 'c2'],['a3', 'b3', 'c3'], ['a3', 'b3', 'c3']]
    >>> gen_freq_table(ds, header, 'Z') is None
    True

    >>> header = ['a', 'b', 'c']
    >>> ds = [['a1', 'b1', 'c1'],['a2', 'b2', 'c2'],['a3', 'b3', 'c3'], ['a3', 'b3', 'c3']]
    >>> fqt = {'b1':(1, 25.0), 'b2':(1, 25.0), 'b3':(2, 50.0)}
    >>> ret_fqt = gen_freq_table(ds, header, 'b')
    >>> all([fqt[k][0] == ret_fqt[k][0] for k in fqt if k in ret_fqt]) and fqt.keys() == ret_fqt.keys()
    True

    >>> header = ['a', 'b', 'c']
    >>> ds = [['a1', 'b1', 'c1'],['a2', 'b2', 'c2'],['a3', 'b3', 'c3'], ['a3', 'b3', 'c3']]
    >>> fqt = {'b3':(2, 50.0), 'b1':(1, 25.0), 'b2':(1, 25.0), }
    >>> ret_fqt = gen_freq_table(ds, header, 'b', sort_by_value=True)
    >>> all([fqt[k][0] == ret_fqt[k][0] for k in fqt if k in ret_fqt]) and fqt.keys() == ret_fqt.keys()
    True

    >>> header = ['a', 'b', 'c']
    >>> ds = [['a1', 'b1', 'c1'],['a2', 'b2', 'c2'],['a3', 'b3', 'c3'], ['a3', 'b3', 'c3']]
    >>> fqt = {'b3':(2, 50.0), 'b2':(1, 25.0), 'b1':(1, 25.0)}
    >>> ret_fqt = gen_freq_table(ds, header, 'b', reverse=True)
    >>> all([fqt[k][0] == ret_fqt[k][0] for k in fqt if k in ret_fqt]) and fqt.keys() == ret_fqt.keys()
    True
    """
    freq_table, total_rows = {}, len(dataset)
    if colname in header:
        # Compute frequency counts
        idx = header.index(colname)
        for row in dataset:
            colval = row[idx]
            if colval not in freq_table:
                freq_table[colval] = [1, 0]
            else:
                freq_table[colval][0] += 1
        # Compute frequency percentages
        for colval in freq_table:
            freq_table[colval][1] = (freq_table[colval][0] / total_rows) * 100
            freq_table[colval] = tuple(freq_table[colval])
        # Sort table
        if sort_by_value:
            return {k: v for k, v in \
                    sorted(freq_table.items(), key=lambda item: item[1][0],
                           reverse=reverse)}
        else:
            return {k: v for k, v in \
                    sorted(freq_table.items(), key=lambda item: item[0],
                           reverse=reverse)}
    return None

def extract_row_range(dataset, rowrange):
    """
    Given  a `dataset`, and a `rowrange` (a two-element tuple|list
    containing integers), extracts, and returns, from `dataset`,
    the set of rows numbered from `rowrange[0]` through `rowrange[1`,
    inclusive. Note row numbering is from 0 through len(dataset)-1.

    :param dataset: list
    :param rowrange: list

    :return: None|list

    >>> dummy = [[],[],[]]
    >>> extract_row_range(dummy, [-1,2]) is None
    True

    >>> dummy = [[],[],[]]
    >>> extract_row_range(dummy, [2,1]) is None
    True

    >>> dummy = [[],[],[]]
    >>> extract_row_range(dummy, [3,1]) is None
    True

    >>> dummy = [[],[],[]]
    >>> extract_row_range(dummy, [1,4]) is None
    True

    >>> orig_ds = [['a1', 'b1', 'c1'],['a2', 'b2', 'c2'],['a3', 'b3', 'c3']]
    >>> exp_ds = [['a2', 'b2', 'c2'], ['a3', 'b3', 'c3']]
    >>> ret_ds = extract_row_range(orig_ds, [1,2])
    >>> ret_ds == exp_ds and ret_ds is not exp_ds
    True

    >>> orig_ds = [['a1', 'b1', 'c1'],['a2', 'b2', 'c2'],['a3', 'b3', 'c3']]
    >>> exp_ds = [['a2', 'b2', 'c2']]
    >>> ret_ds = extract_row_range(orig_ds, [1,1])
    >>> ret_ds == exp_ds and ret_ds is not exp_ds
    True

    """
    lb, ub = rowrange
    if lb < 0 or lb > ub: return None
    if ub < lb or ub > len(dataset)-1: return None
    return dataset[lb:(ub+1)] if lb != ub else [dataset[lb]]

if __name__ == "__main__":
    doctest.testmod()

