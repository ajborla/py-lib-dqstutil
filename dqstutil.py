import doctest

def _is_valid_colnames(header, colnames):
    """
    Given a list of column name, `colnames`, returns True if each
    element is also in the list, `header`.

    :param header: list
    :param colnames: list
    :return: bool

    >>> _is_valid_colnames(['a', 'b', 'c'], ['b', 'c'])
    True

    >>> _is_valid_colnames(['a', 'b', 'c'], ['e', 'c'])
    False

    >>> _is_valid_colnames(['a', 'b', 'c'], {})
    False

    >>> _is_valid_colnames(['a', 'b', 'c'], [])
    False

    >>> _is_valid_colnames(['a', 'b', 'c'], [1, 2])
    False
    """
    return \
        type(header) is list \
        and len(header) > 0 \
        and type(colnames) is list \
        and len(colnames) > 0 \
        and all(map(lambda x: x in header, colnames))

def is_numeric(s):
    """
    Given `s`, returns True if it is either a numeric type, or a
    numeric-convertible string.

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
        return \
            type(s) is int \
            or type(s) is float \
            or type(s) is complex
    else:
        return \
            s.isnumeric() \
            or to_complex()

def is_possible_date(s):
    """
    Given `s`, returns True if it is possibly a date-convertible
    string.

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
    month_prefixes = [
        'jan', 'feb', 'mar', 'apr',
        'may', 'jun', 'jul', 'aug',
        'sep', 'oct', 'nov', 'dec'
    ]
    s = s.lower()
    is_date_separator = lambda c: c == '/' or c == '-'
    # Valid candidate must contain a month name or exactly two
    # date separator characters
    return \
        any(map(lambda m: m in s, month_prefixes)) \
        or len(list(filter(is_date_separator, s))) == 2

def is_possible_numeric(s):
    """
    Given `s`, returns True if it is possibly a numeric-convertible
    string, such as a currency value or comma-separted numeric, or a
    suffixed value (such as a measurement). Note that version strings
    (often having two or more decimal points) are NOT considered
    possible numerics.

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
    # Tests for string `s` numeric-format compliance
    contains_one_or_more_digits = \
        any(map(lambda c: c.isdigit(), s))
    contains_zero_or_one_decimal_point = \
        len(list(filter(lambda c: c == '.', s))) < 2
    contains_zero_or_one_dollar_sign = \
        len(list(filter(lambda c: c == '$', s))) < 2
    is_not_possible_date = \
        not is_possible_date(s)
    # Apply tests, return result
    return \
        contains_one_or_more_digits \
        and is_not_possible_date \
        and contains_zero_or_one_decimal_point \
        and contains_zero_or_one_dollar_sign

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

def inspect_dataset(dataset, header, generate_report=True,
                    printer=print):
    """
    Given `dataset` and `header`, inspects `dataset` collecting
    metadata, and either returns metadata or generates, and prints,
    a report. By default, data is printed using the built-in `print`
    function, but allows an alternate function (such as `pprint`) to
    be used via the `printer` argument.

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
    :param printer: function

    :return: None|tuple(list,dict,dict,dict)

    >>> header = ['a', 'b', 'c']
    >>> dataset = [ \
            ['a1', 'b1', 'c1'], \
            ['a2', 'c2'], \
            ['a3', 'b3', 'c3'], \
            ['a4', 'bib', '3'], \
            ['ay', 'bib', 'x'], \
            ['ay', 'bib', 'x']  \
        ]
    >>> rowskip, columns, uniques, duplicates = \
            inspect_dataset(dataset, header, generate_report=False)
    >>> (rowskip, columns, uniques, duplicates)
    ([1], \
{'a': {'PN': 3, 'T': 2}, 'b': {'PN': 2, 'T': 3}, \
'c': {'PN': 2, 'N': 1, 'T': 2}}, \
{'a': 1, 'b': 1, 'c': 1}, {'a': 1, 'b': 2, 'c': 1})

    >>> header = ['a', 'b', 'c']
    >>> dataset = [ \
            ['a1', 'b1', 'c1'], \
            ['a2', 'c2'], \
            ['a3', 'b3', 'c3'], \
            ['a4', 'bib', '3'], \
            ['ay', 'bib', 'x'], \
            ['ay', 'bib', 'x'] \
        ]
    >>> inspect_dataset(dataset, header, generate_report=True)
    Invalid (incorrect length) row numbers:[1]
    <BLANKLINE>
    Tentative column type(s) [T - text, N - numeric, \
PN - possible numeric, PD - possible date]:
    <BLANKLINE>
    {'a': {'PN': 3, 'T': 2}, 'b': {'PN': 2, 'T': 3}, \
'c': {'PN': 2, 'N': 1, 'T': 2}}
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
        row_rep_header = \
            'Invalid (incorrect length) row numbers:'
        col_rep_header = \
            'Tentative column type(s) [T - text, N - numeric,' \
            ' PN - possible numeric, PD - possible date]:'
        unique_rep_header = \
            'Unique value counts (non-numeric and non-date columns' \
            ' only):'
        dup_rep_header = \
            'Duplicate value counts (non-numeric and non-date' \
            ' columns only):'
        print(row_rep_header, end='')
        printer(rowskip)
        print('', col_rep_header, '', sep='\n')
        printer(columns)
        print('', unique_rep_header, '', sep='\n')
        printer(uniques)
        print('', dup_rep_header, '', sep='\n')
        printer(duplicates)
    else:
        # Return collected metadata as tuple
        return (rowskip, columns, uniques, duplicates)

def extract_unique_values(values, sort=False, sep='|'):
    """
    Given a list, `values`, a type-specific unique-value determination
    algorithm is selected, and applied, with the unique values returned
    as a list, optionally sorted in ascending order if `sort` is set.
    Optional, too, is `sep`, used as a separator where `values`'
    elements are multi-(non-list)-element lists (elements are joined
    to create the entity on which uniqueness is determined).

    Return list comprises the unique values in `values`, and in the
    case where elements are lists, these are the list-contained values.
    Refer to the tests for examples.

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

    >>> values = [ \
            ['a1'], ['b1'], ['c1'], \
            ['a2'], ['b1'], ['c1'], \
            ['a1'], ['b2'], ['c1'] \
        ]
    >>> uniques = ['a1', 'b1', 'c1', 'a2', 'b2']
    >>> sorted(extract_unique_values(values)) == sorted(uniques)
    True

    >>> values = [[1], [2], [3], [1]]
    >>> uniques = [1, 2, 3]
    >>> extract_unique_values(values) == uniques
    True

    >>> values = [ \
            ['a1', 'b1', 'c1'], \
            ['a2', 'b2', 'c2'], \
            ['a3', 'b3', 'c3'], \
            ['a2', 'b2', 'c2'] \
        ]
    >>> uniques = ['a1|b1|c1', 'a2|b2|c2', 'a3|b3|c3']
    >>> sorted(extract_unique_values(values)) == sorted(uniques)
    True

    >>> values = [['a1'], ['b1'], [], ['a2'], ['b1']]
    >>> extract_unique_values(values) is None
    True

    >>> values = [['a1'], ['b1'], 0, ['a2'], ['b1']]
    >>> extract_unique_values(values) is None
    True

    >>> values = [ \
            ['a1', 'b1', 'c1'], \
            [], \
            ['a3', 'b3', 'c3'], \
            ['a2', 'b2', 'c2'] \
        ]
    >>> extract_unique_values(values) is None
    True

    >>> values = [ \
            ['a1', 'b1', 'c1'], \
            ['a2', 'c2'], \
            ['a3', 'b3', 'c3'], \
            ['a2', 'b2', 'c2'] \
        ]
    >>> extract_unique_values(values) is None
    True

    >>> values = [ \
            ['a1', 'b1', 'c1'], \
            ['a2', 0, 'c2'], \
            ['a3', 'b3', 'c3'], \
            ['a2', 'b2', 'c2'] \
        ]
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
        # and do not, themselves, contain lists
        if elem_len == 0:
            return None
        contains_no_list = \
            lambda v: all(map(lambda x: type(x) is not list, v))
        is_homogenous = \
            lambda v, w: all(map(lambda x: type(x) is type(w), v))
        if not all(map(lambda v: len(v) == elem_len \
           and contains_no_list(v) \
           and is_homogenous(v, v[0]), values)):
                return None
        # Return values depend on sublist element number
        if elem_len > 1:
            # Unique values returned as string, concatenation of
            # individual values
            to_str = lambda v: map(lambda x: str(x), v)
            uniques = \
                [sep.join(to_str(v)) \
                    for v in set([tuple(v) for v in values])]
        else:
            # Unique values returned as original type
            uniques = \
                [v[0] for v in set([tuple(v) for v in values])]
    else:
        # Non-list element type; unique values returned as original
        # type
        uniques = \
            [v for i, v in enumerate(values) if v not in values[:i]]
    # Sorted (ascending) unique value list, if requested
    return sorted(uniques) if sort else uniques

def gen_freq_table(dataset, header, colname, sort_by_value=False,
                   reverse=False):
    """
    Given  a `dataset`, its `header`, a column name, `colname`,
    generates a frequency table keyed by `colname`, and including both
    the count and relative percentage as a tuple. Returned table is
    sorted by key, that is, by `colname`, ascending. The value of
    optional boolean arguments, `sort_by_value` and `reverse`,
    determine alternate ordering of the table entries.

    :param dataset: list
    :param header: list
    :param colname: str
    :param sort_by_value: bool
    :param reverse: bool

    :return: dict

    >>> header = ['a', 'b', 'c']
    >>> ds = [ \
            ['a1', 'b1', 'c1'], \
            ['a2', 'b2', 'c2'], \
            ['a3', 'b3', 'c3'], \
            ['a3', 'b3', 'c3'] \
        ]
    >>> gen_freq_table(ds, header, 'Z') is None
    True

    >>> header = ['a', 'b', 'c']
    >>> ds = [ \
            ['a1', 'b1', 'c1'], \
            ['a2', 'b2', 'c2'], \
            ['a3', 'b3', 'c3'], \
            ['a3', 'b3', 'c3'] \
        ]
    >>> fqt = {'b1':(1, 25.0), 'b2':(1, 25.0), 'b3':(2, 50.0)}
    >>> ret_fqt = gen_freq_table(ds, header, 'b')
    >>> all([fqt[k][0] == ret_fqt[k][0] \
            for k in fqt if k in ret_fqt]) \
                            and fqt.keys() == ret_fqt.keys()
    True

    >>> header = ['a', 'b', 'c']
    >>> ds = [ \
            ['a1', 'b1', 'c1'], \
            ['a2', 'b2', 'c2'], \
            ['a3', 'b3', 'c3'], \
            ['a3', 'b3', 'c3'] \
        ]
    >>> fqt = {'b3':(2, 50.0), 'b1':(1, 25.0), 'b2':(1, 25.0), }
    >>> ret_fqt = gen_freq_table(ds, header, 'b', sort_by_value=True)
    >>> all([fqt[k][0] == ret_fqt[k][0] \
            for k in fqt if k in ret_fqt]) \
                            and fqt.keys() == ret_fqt.keys()
    True

    >>> header = ['a', 'b', 'c']
    >>> ds = [ \
            ['a1', 'b1', 'c1'], \
            ['a2', 'b2', 'c2'], \
            ['a3', 'b3', 'c3'], \
            ['a3', 'b3', 'c3'] \
        ]
    >>> fqt = {'b3':(2, 50.0), 'b2':(1, 25.0), 'b1':(1, 25.0)}
    >>> ret_fqt = gen_freq_table(ds, header, 'b', reverse=True)
    >>> all([fqt[k][0] == ret_fqt[k][0] \
            for k in fqt if k in ret_fqt]) \
                            and fqt.keys() == ret_fqt.keys()
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
            freq_table[colval][1] = \
                (freq_table[colval][0] / total_rows) * 100
            freq_table[colval] = tuple(freq_table[colval])
        # Sort table
        if sort_by_value:
            return {k: v for k, v in \
                    sorted(freq_table.items(),
                           key=lambda item: item[1][0],
                           reverse=reverse)}
        else:
            return {k: v for k, v in \
                    sorted(freq_table.items(),
                           key=lambda item: item[0],
                           reverse=reverse)}
    # Fallthrough case
    return None

def add_column(dataset, header, colname, coldata, inplace=False):
    """
    Given  a `dataset`, its `header`, and a single column name,
    `colname`, and a list of data, `coldata` with an element for
    each row in `dataset`, adds `colname` to the dataset and fills
    it with the data from `coldata`. A copy of the dataset, and
    header is modified unless `inplace` is True, in which case,
    the original dataset and original header, with modifications,
    are returned. Note dataset copy is a copy of the container and
    copies of the elements too.

    :param dataset: list
    :param header: list
    :param colname: str
    :param coldata: list
    :param inplace: bool

    :return: list, list|None, None

    >>> header = ['a', 'b', 'c']
    >>> dummy = [[],[],[]]
    >>> ret_ds, ret_hd = add_column(dummy, header, [], dummy)
    >>> ret_ds is None and ret_hd is None
    True

    >>> header = ['a', 'b', 'c']
    >>> dummy = [[],[],[]]
    >>> ret_ds, ret_hd = add_column(dummy, header, '', dummy)
    >>> ret_ds is None and ret_hd is None
    True

    >>> header = ['a', 'b', 'c']
    >>> dummy = [[],[],[]]
    >>> ret_ds, ret_hd = add_column(dummy, header, 'a', dummy)
    >>> ret_ds is None and ret_hd is None
    True

    >>> # Add column 'd' to dataset and header copies, return both
    >>> orig_hd = ['a', 'b', 'c']
    >>> new_hd = ['a', 'b', 'c', 'd']
    >>> orig_ds = [ \
            ['a1', 'b1', 'c1'], \
            ['a2', 'b2', 'c2'], \
            ['a3', 'b3', 'c3'] \
        ]
    >>> new_ds = [ \
            ['a1', 'b1', 'c1', 'd1'], \
            ['a2', 'b2', 'c2', 'd2'], \
            ['a3', 'b3', 'c3', 'd3'] \
        ]
    >>> coldata = ['d1', 'd2', 'd3']
    >>> ret_ds, ret_hd = add_column(orig_ds, orig_hd, 'd', coldata)
    >>> cmpds = lambda: all(map(lambda p, q: p is not q \
                                             and p == q, \
                                ret_ds, new_ds))
    >>> cmphd = lambda: all(map(lambda p, q: p == q, \
                                ret_hd, new_hd))
    >>> ret_ds is not orig_ds \
        and cmpds() \
        and ret_hd is not orig_hd \
        and cmphd()
    True

    >>> # Add column 'd' to dataset and header originals, return both
    >>> orig_hd = ['a', 'b', 'c']
    >>> new_hd = ['a', 'b', 'c', 'd']
    >>> orig_ds = [ \
            ['a1', 'b1', 'c1'], \
            ['a2', 'b2', 'c2'], \
            ['a3', 'b3', 'c3'] \
        ]
    >>> new_ds = [ \
            ['a1', 'b1', 'c1', 'd1'], \
            ['a2', 'b2', 'c2', 'd2'], \
            ['a3', 'b3', 'c3', 'd3'] \
        ]
    >>> coldata = ['d1', 'd2', 'd3']
    >>> ret_ds, ret_hd = add_column(orig_ds, orig_hd, 'd', coldata, \
                                    inplace=True)
    >>> cmpds = lambda: all(map(lambda p,q,r: p is q \
                                              and p == q \
                                              and p == r, \
                                ret_ds, orig_ds, new_ds))
    >>> cmphd = lambda: all(map(lambda p,q,r: p == q \
                                              and p == r, \
                                ret_hd, orig_hd, new_hd))
    >>> ret_ds is orig_ds \
        and cmpds() \
        and ret_hd is orig_hd \
        and cmphd()
    True
    """
    if type(colname) is str and len(colname) > 0 \
       and colname not in header \
       and len(coldata) == len(dataset):
        # `inplace` flag determines whether originals or copies
        # modified
        dataset = dataset if inplace else [x[:] for x in dataset]
        header = header if inplace else header[:]
        # Column is appended to dataset, column name appended to
        # header
        header.append(colname)
        for row, newcol in zip(dataset, coldata):
            row.append(newcol)
        return dataset, header
    # Fallthrough case
    return None, None

def remove_column(dataset, header, colname, inplace=False):
    """
    Given  a `dataset`, its `header`, and a single column name,
    `colname`, removes the nominated column from `dataset` and
    from the `header`. A copy of the dataset, and of the header,
    is modified and returned, unless `inplace` is True, in
    which case, the original dataset and original header, with
    modifications, are returned. Note dataset copy is a copy of
    the container and copies of the elements too.

    :param dataset: list
    :param header: list
    :param colname: str
    :param inplace: bool

    :return: list, list|None, None

    >>> header = ['a', 'b', 'c']
    >>> dummy = [[],[],[]]
    >>> ret_ds, ret_hd = remove_column(dummy, header, [])
    >>> ret_ds is None and ret_hd is None
    True

    >>> header = ['a', 'b', 'c']
    >>> dummy = [[],[],[]]
    >>> ret_ds, ret_hd = remove_column(dummy, header, 'd')
    >>> ret_ds is None and ret_hd is None
    True

    >>> # Remove 'b' column from dataset, header, return both copies
    >>> orig_hd = ['a', 'b', 'c']
    >>> new_hd = ['a', 'c']
    >>> orig_ds = [ \
            ['a1', 'b1', 'c1'], \
            ['a2', 'b2', 'c2'], \
            ['a3', 'b3', 'c3'] \
        ]
    >>> new_ds = [ \
            ['a1', 'c1'], \
            ['a2', 'c2'], \
            ['a3', 'c3'] \
        ]
    >>> ret_ds, ret_hd = remove_column(orig_ds, orig_hd, 'b')
    >>> cmpds = lambda: all(map(lambda p, q: p is not q \
                                             and p == q, \
                                ret_ds, new_ds))
    >>> cmphd = lambda: all(map(lambda p, q: p == q, \
                                ret_hd, new_hd))
    >>> ret_ds is not orig_ds \
        and cmpds() \
        and ret_hd is not orig_hd \
        and cmphd()
    True

    >>> # Remove 'b' column from dataset, header, return both originals
    >>> orig_hd = ['a', 'b', 'c']
    >>> new_hd = ['a', 'c']
    >>> orig_ds = [ \
            ['a1', 'b1', 'c1'], \
            ['a2', 'b2', 'c2'], \
            ['a3', 'b3', 'c3'] \
        ]
    >>> new_ds = [ \
            ['a1', 'c1'], \
            ['a2', 'c2'], \
            ['a3', 'c3'] \
        ]
    >>> ret_ds, ret_hd = remove_column(orig_ds, orig_hd, 'b', \
                                       inplace=True)
    >>> cmpds = lambda: all(map(lambda p, q, r: p is q \
                                                and p == q \
                                                and p == r, \
                                ret_ds, orig_ds, new_ds))
    >>> cmphd = lambda: all(map(lambda p, q, r: p == q \
                                                and p == r, \
                                ret_hd, orig_hd, new_hd))
    >>> ret_ds is orig_ds \
        and cmpds() \
        and ret_hd is orig_hd \
        and cmphd()
    True
    """
    if type(colname) is str and colname in header:
        # `inplace` flag determines whether originals or copies
        # modified
        dataset = dataset if inplace else [x[:] for x in dataset]
        header = header if inplace else header[:]
        idx = header.index(colname)
        for row in dataset:
            del row[idx]
        del header[idx]
        return dataset, header
    # Fallthrough case
    return None, None,

def modify_column(dataset, header, colname, coldata, inplace=False):
    """
    Given  a `dataset`, its `header`, and a single column name,
    `colname`, and a list of data, `coldata` with an element for
    each row in `dataset`, replaces the data in the column,
    `colname` with the data from `coldata`. A copy of the dataset,
    is modified unless `inplace` is True, in which case, the
    original dataset, with modifications, and the original header,
    are returned. Note dataset copy is a copy of the container and
    copies of the elements too.

    :param dataset: list
    :param header: list
    :param colname: str
    :param coldata: list
    :param inplace: bool

    :return: list, list|None, None

    >>> header = ['a', 'b', 'c']
    >>> dummy = [[],[],[]]
    >>> ret_ds, ret_hd = modify_column(dummy, header, [], dummy)
    >>> ret_ds is None and ret_hd is None
    True

    >>> header = ['a', 'b', 'c']
    >>> dummy = [[],[],[]]
    >>> ret_ds, ret_hd = modify_column(dummy, header, '', dummy)
    >>> ret_ds is None and ret_hd is None
    True

    >>> header = ['a', 'b', 'c']
    >>> dummy = [[],[],[]]
    >>> ret_ds, ret_hd = modify_column(dummy, header, 'd', dummy)
    >>> ret_ds is None and ret_hd is None
    True

    >>> # Modify column 'b' in dataset copy, return copies
    >>> header = ['a', 'b', 'c']
    >>> orig_ds = [ \
            ['a1', 'b1', 'c1'], \
            ['a2', 'b2', 'c2'], \
            ['a3', 'b3', 'c3'] \
        ]
    >>> new_ds = [ \
            ['a1', 'X1', 'c1'], \
            ['a2', 'X2', 'c2'], \
            ['a3', 'X3', 'c3'] \
        ]
    >>> coldata = ['X1', 'X2', 'X3']
    >>> ret_ds, ret_hd = modify_column(orig_ds, header, 'b', coldata)
    >>> cmpds = lambda: all(map(lambda p, q: p is not q \
                                             and p == q, \
                                ret_ds, new_ds))
    >>> ret_ds is not orig_ds and cmpds()
    True

    >>> # Modify column 'b' in dataset, return originals
    >>> header = ['a', 'b', 'c']
    >>> orig_ds = [ \
            ['a1', 'b1', 'c1'], \
            ['a2', 'b2', 'c2'], \
            ['a3', 'b3', 'c3'] \
        ]
    >>> new_ds = [ \
            ['a1', 'X1', 'c1'], \
            ['a2', 'X2', 'c2'], \
            ['a3', 'X3', 'c3'] \
        ]
    >>> coldata = ['X1', 'X2', 'X3']
    >>> ret_ds, ret_hd = modify_column(orig_ds, header, 'b', coldata, \
                                       inplace=True)
    >>> cmpds = lambda: all(map(lambda p, q, r: p is q \
                                                and p == q \
                                                and p == r, \
                                ret_ds, orig_ds, new_ds))
    >>> ret_ds is orig_ds and cmpds()
    True
    """
    if type(colname) is str and len(colname) > 0 \
       and colname in header \
       and len(coldata) == len(dataset):
        # `inplace` flag determines whether originals or copies
        # modified
        dataset = dataset if inplace else [x[:] for x in dataset]
        header = header if inplace else header[:]
        # Column is modified
        idx = header.index(colname)
        for row, newcol in zip(dataset, coldata):
            row[idx] = newcol
        return dataset, header
    # Fallthrough case
    return None, None

def transform_column(dataset, header, colname, transform,
                     inplace=False):
    """
    Given  a `dataset`, its `header`, a column name, `colname`, and a
    1 or 3-argument function, `transform`, applies the function to
    column `colname` (to all dataset rows) replacing its contents. A
    copy of the dataset is modified unless `inplace` is True, in
    which case, the original dataset, with modifications, and the
    original header, are returned. Note dataset copy is a copy of the
    container and copies of the elements too.

    For each row of the dataset, `transform` receives `colname`'s
    contents, and, if implemented as a 3-argument function, receives
    the current row, and the header, so allowing access to other
    columns, and tranforms it; its return value then replaces it.
    Example function implementations:

        `lambda c: c.lower()`
        `def transform(c): return c.lower()`

        `lambda c, r, h: c + r[h.index('c2')]`
        `def transform(c, r, h): return c + r[h.index('c2')]`

    :param dataset: list
    :param header: list
    :param colname: str
    :param transform: function
    :param inplace: bool

    :return: list, list|None, None

    >>> header = ['a', 'b', 'c']
    >>> dummy = [[],[],[]]
    >>> transform = lambda x: None
    >>> ret_ds, ret_hd = transform_column(dummy, header, [], transform)
    >>> ret_ds is None and ret_hd is None
    True

    >>> header = ['a', 'b', 'c']
    >>> dummy = [[],[],[]]
    >>> transform = lambda x: None
    >>> ret_ds, ret_hd = transform_column(dummy, header, '', transform)
    >>> ret_ds is None and ret_hd is None
    True

    >>> header = ['a', 'b', 'c']
    >>> dummy = [[],[],[]]
    >>> transform = lambda x: None
    >>> ret_ds, ret_hd = transform_column(dummy, header, 'd', transform)
    >>> ret_ds is None and ret_hd is None
    True

    >>> header = ['a', 'b', 'c']
    >>> dummy = [[],[],[]]
    >>> transform = {}
    >>> ret_ds, ret_hd = transform_column(dummy, header, 'a', transform)
    >>> ret_ds is None and ret_hd is None
    True

    >>> header = ['a', 'b', 'c']
    >>> dummy = [[],[],[]]
    >>> transform = lambda x,y: None
    >>> ret_ds, ret_hd = transform_column(dummy, header, 'a', transform)
    >>> ret_ds is None and ret_hd is None
    True

    >>> # Copy of dataset is modified
    >>> header = ['a', 'b', 'c']
    >>> orig_ds = [ \
            ['a1', 'b1', 'c1'], \
            ['a2', 'b2', 'c2'], \
            ['a3', 'b3', 'c3'] \
        ]
    >>> new_ds = [ \
            ['a1', 'B1', 'c1'], \
            ['a2', 'B2', 'c2'], \
            ['a3', 'B3', 'c3'] \
        ]
    >>> ret_ds, _ = transform_column(orig_ds, header, 'b', \
                                     lambda x: x.upper())
    >>> cmpds = lambda: all(map(lambda p, q: p is not q \
                                             and p == q, \
                                ret_ds, new_ds))
    >>> ret_ds is not orig_ds and cmpds()
    True

    >>> # Original dataset is modified
    >>> header = ['a', 'b', 'c']
    >>> orig_ds = [ \
            ['a1', 'b1', 'c1'], \
            ['a2', 'b2', 'c2'], \
            ['a3', 'b3', 'c3'] \
        ]
    >>> new_ds = [ \
            ['a1', 'B1', 'c1'], \
            ['a2', 'B2', 'c2'], \
            ['a3', 'B3', 'c3'] \
        ]
    >>> ret_ds, _ = transform_column(orig_ds, header, 'b', \
                                     lambda x: x.upper(), \
                                     inplace=True)
    >>> cmpds = lambda: all(map(lambda p, q, r: p is q \
                                                and p == q \
                                                and p == r, \
                                ret_ds, orig_ds, new_ds))
    >>> ret_ds is orig_ds and cmpds()
    True
    """
    if type(colname) is str and len(colname) > 0 \
       and colname in header \
       and type(transform) is type(lambda x: None):
        # Check expected arity of `transform` function
        targc = transform.__code__.co_argcount
        if targc not in [1, 3]:
            return None, None
        # `inplace` flag determines whether originals or copies
        # modified
        dataset = dataset if inplace else [x[:] for x in dataset]
        header = header if inplace else header[:]
        # Column is transformed using `transform` function
        idx = header.index(colname)
        for row in dataset:
            colval = row[idx]
            row[idx] = \
                transform(colval) if targc == 1 else \
                transform(colval, row, header)
        return dataset, header
    # Fallthrough case
    return None, None

def remove_columns(dataset, header, colnames, inplace=False):
    """
    Given a `dataset`, its `header`, and a list of column names,
    `colnames`, removes the nominated columns from `dataset` and
    from the `header`. A copy of the dataset, and of the header,
    is modified and returned, unless `inplace` is True, in
    which case, the original dataset and original header, with
    modifications, are returned. Note dataset copy is a copy of
    the container and copies of the elements too.

    :param dataset: list
    :param header: list
    :param colnames: list
    :param inplace: bool

    :return: list, list|None, None

    >>> header = ['a', 'b', 'c']
    >>> dummy = [[],[],[]]
    >>> ret_ds, ret_hd = remove_columns(dummy, header, {})
    >>> ret_ds is None and ret_hd is None
    True

    >>> header = ['a', 'b', 'c']
    >>> dummy = [[],[],[]]
    >>> ret_ds, ret_hd = remove_columns(dummy, header, [])
    >>> ret_ds is None and ret_hd is None
    True

    >>> header = ['a', 'b', 'c']
    >>> dummy = [[],[],[]]
    >>> ret_ds, ret_hd = remove_columns(dummy, header, ['d'])
    >>> ret_ds is None and ret_hd is None
    True

    >>> # Remove 'b' column from dataset, header, return copies
    >>> orig_hd = ['a', 'b', 'c']
    >>> new_hd = ['a', 'c']
    >>> orig_ds = [ \
            ['a1', 'b1', 'c1'], \
            ['a2', 'b2', 'c2'], \
            ['a3', 'b3', 'c3'] \
        ]
    >>> new_ds = [ \
            ['a1', 'c1'], \
            ['a2', 'c2'], \
            ['a3', 'c3'] \
        ]
    >>> ret_ds, ret_hd = remove_column(orig_ds, orig_hd, 'b')
    >>> cmpds = lambda: all(map(lambda p, q: p is not q \
                                             and p == q, \
                                ret_ds, new_ds))
    >>> cmphd = lambda: all(map(lambda p, q: p == q, \
                                ret_hd, new_hd))
    >>> ret_ds is not orig_ds \
        and cmpds() \
        and ret_hd is not orig_hd \
        and cmphd()
    True

    >>> # Remove 'b' column from dataset, header, return originals
    >>> orig_hd = ['a', 'b', 'c']
    >>> new_hd = ['a', 'c']
    >>> orig_ds = [ \
            ['a1', 'b1', 'c1'], \
            ['a2', 'b2', 'c2'], \
            ['a3', 'b3', 'c3'] \
        ]
    >>> new_ds = [ \
            ['a1', 'c1'], \
            ['a2', 'c2'], \
            ['a3', 'c3'] \
        ]
    >>> ret_ds, ret_hd = remove_column(orig_ds, orig_hd, 'b', \
                                       inplace=True)
    >>> cmpds = lambda: all(map(lambda p, q, r: p is q \
                                                and p == q \
                                                and p == r, \
                                ret_ds, orig_ds, new_ds))
    >>> cmphd = lambda: all(map(lambda p, q, r: p == q \
                                                and p == r, \
                                ret_hd, orig_hd, new_hd))
    >>> ret_ds is orig_ds \
        and cmpds() \
        and ret_hd is orig_hd \
        and cmphd()
    True

    >>> # Remove 'a', 'c' column from dataset, header, return copies
    >>> orig_hd = ['a', 'b', 'c']
    >>> new_hd = ['b']
    >>> orig_ds = [ \
            ['a1', 'b1', 'c1'], \
            ['a2', 'b2', 'c2'], \
            ['a3', 'b3', 'c3'] \
        ]
    >>> new_ds = [ \
            ['b1'], \
            ['b2'], \
            ['b3'] \
        ]
    >>> ret_ds, ret_hd = remove_columns(orig_ds, orig_hd, ['a', 'c'])
    >>> cmpds = lambda: all(map(lambda p, q: p is not q \
                                             and p == q, \
                                ret_ds, new_ds))
    >>> cmphd = lambda: all(map(lambda p, q: p == q, \
                                ret_hd, new_hd))
    >>> ret_ds is not orig_ds \
        and cmpds() \
        and ret_hd is not orig_hd \
        and cmphd()
    True

    >>> # Remove 'a', 'c' column from dataset, header, return originals
    >>> orig_hd = ['a', 'b', 'c']
    >>> new_hd = ['b']
    >>> orig_ds = [ \
            ['a1', 'b1', 'c1'], \
            ['a2', 'b2', 'c2'], \
            ['a3', 'b3', 'c3'] \
        ]
    >>> new_ds = [ \
            ['b1'], \
            ['b2'], \
            ['b3'] \
        ]
    >>> ret_ds, ret_hd = remove_columns(orig_ds, orig_hd, ['a', 'c'], \
                                        inplace=True)
    >>> cmpds = lambda: all(map(lambda p, q, r: p is q \
                                                and p == q \
                                                and p == r, \
                                ret_ds, orig_ds, new_ds))
    >>> cmphd = lambda: all(map(lambda p, q, r: p == q \
                                                and p == r, \
                                ret_hd, orig_hd, new_hd))
    >>> ret_ds is orig_ds \
        and cmpds() \
        and ret_hd is orig_hd \
        and cmphd()
    True

    >>> # Remove all columns from dataset, header, return copies
    >>> orig_hd = ['a', 'b', 'c']
    >>> new_hd = []
    >>> orig_ds = [ \
            ['a1', 'b1', 'c1'], \
            ['a2', 'b2', 'c2'], \
            ['a3', 'b3', 'c3'] \
        ]
    >>> new_ds = []
    >>> ret_ds, ret_hd = remove_columns(orig_ds, orig_hd, ['a', 'b', 'c'])
    >>> cmpds = lambda: all(map(lambda p, q: p is not q \
                                             and p == q, \
                                ret_ds, new_ds))
    >>> cmphd = lambda: all(map(lambda p, q: p == q, \
                                ret_hd, new_hd))
    >>> ret_ds is not orig_ds \
        and cmpds() \
        and ret_hd is not orig_hd \
        and cmphd()
    True

    >>> # Remove all columns from dataset, header, return originals
    >>> orig_hd = ['a', 'b', 'c']
    >>> new_hd = []
    >>> orig_ds = [ \
            ['a1', 'b1', 'c1'], \
            ['a2', 'b2', 'c2'], \
            ['a3', 'b3', 'c3'] \
        ]
    >>> new_ds = []
    >>> ret_ds, ret_hd = remove_columns(orig_ds, orig_hd, ['a', 'c'], \
                                        inplace=True)
    >>> cmpds = lambda: all(map(lambda p, q, r: p is q \
                                                and p == q \
                                                and p == r, \
                                ret_ds, orig_ds, new_ds))
    >>> cmphd = lambda: all(map(lambda p, q, r: p == q \
                                                and p == r, \
                                ret_hd, orig_hd, new_hd))
    >>> ret_ds is orig_ds \
        and cmpds() \
        and ret_hd is orig_hd \
        and cmphd()
    True
    """
    if _is_valid_colnames(header, colnames):
        # `inplace` flag determines whether originals or copies
        # modified
        dataset = dataset if inplace else [x[:] for x in dataset]
        header = header if inplace else header[:]
        # Reverse column names to ensure higher indexes deleted
        # before lower indexes, else for-loop traversal is
        # compromised
        idxs = []
        for colname in colnames:
            idxs.append(header.index(colname))
        idxs.sort(key=int, reverse=True)
        # Perform column deletion dataset, update header
        for row in dataset:
            for idx in idxs:
                del row[idx]
        for idx in idxs:
            del header[idx]
        return dataset, header
    # Fallthrough case
    return None, None,

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

    >>> orig_ds = [ \
            ['a1', 'b1', 'c1'], \
            ['a2', 'b2', 'c2'], \
            ['a3', 'b3', 'c3'] \
        ]
    >>> exp_ds = [ \
            ['a2', 'b2', 'c2'], \
            ['a3', 'b3', 'c3'] \
        ]
    >>> ret_ds = extract_row_range(orig_ds, [1,2])
    >>> ret_ds == exp_ds and ret_ds is not exp_ds
    True

    >>> orig_ds = [ \
            ['a1', 'b1', 'c1'], \
            ['a2', 'b2', 'c2'], \
            ['a3', 'b3', 'c3'] \
        ]
    >>> exp_ds = [ \
            ['a2', 'b2', 'c2'], \
        ]
    >>> ret_ds = extract_row_range(orig_ds, [1,1])
    >>> ret_ds == exp_ds and ret_ds is not exp_ds
    True
    """
    lb, ub = rowrange
    if lb < 0 or lb > ub: return None
    if ub < lb or ub > len(dataset)-1: return None
    return dataset[lb:(ub+1)] if lb != ub else [dataset[lb]]

def extract_rows(dataset, header, predicate, colnames=None):
    """
    Given  a `dataset`, its `header`, a 2-argument function,
    `predicate`, and, optionally, a list of column names, `colnames`,
    applies the function to each row of the dataset, and retains the
    row if the function application returns True.

    If `colnames` is supplied, keeps the nominated columns from the
    retained rows, discarding all others. A copy of the header is
    updated to reflect these changes. In all cases copies of the dataset
    and header (whether modified or not) are returned (there is no
    'inplace' modification).

    For each row of the dataset, `predicate` receives the row, as well
    as `header`. `predicate` uses the arguments to craft a boolean
    expression that returns True if the row is to be retained. Example
    function implementations:

      `lambda row, header: row[header.index('c')] > 'c1'`
      `def predicate(row, header): return row[header.index('c')] > 'c1'`

    :param dataset: list
    :param header: list
    :param predicate: function
    :param colnames: None|ist

    :return: list, list

    >>> # Pass non-function predicate
    >>> header = ['a', 'b', 'c']
    >>> dummy = [[],[],[]]
    >>> predicate = []
    >>> extract_rows(dummy, header, predicate) is None
    True

    >>> # Pass 3-arg predicate
    >>> header = ['a', 'b', 'c']
    >>> dummy = [[],[],[]]
    >>> predicate = lambda x,y,z: None
    >>> extract_rows(dummy, header, predicate) is None
    True

    >>> # Extract all rows
    >>> header = ['a', 'b', 'c']
    >>> orig_ds = [['a1', 'b1', 'c1'],['a2', 'b2', 'c2'],['a3', 'b3', 'c3']]
    >>> exp_ds = [['a1', 'b1', 'c1'],['a2', 'b2', 'c2'],['a3', 'b3', 'c3']]
    >>> predicate = lambda row, header: True
    >>> ret_ds, _ = extract_rows(orig_ds, header, predicate)
    >>> ret_ds is not orig_ds and ret_ds == exp_ds
    True

    >>> # Extract selected rows
    >>> header = ['a', 'b', 'c']
    >>> orig_ds = [['a1', 'b1', 'c1'],['a2', 'b2', 'c2'],['a3', 'b3', 'c3']]
    >>> exp_ds = [['a2', 'b2', 'c2'],['a3', 'b3', 'c3']]
    >>> predicate = lambda row, header: row[header.index('c')] > 'c1'
    >>> ret_ds, _ = extract_rows(orig_ds, header, predicate)
    >>> ret_ds is not orig_ds and ret_ds == exp_ds
    True

    >>> # `colnames` is an empty list
    >>> header = ['a', 'b', 'c']
    >>> dummy = [['a1', 'b1', 'c1'],['a2', 'b2', 'c2'],['a3', 'b3', 'c3']]
    >>> predicate = lambda row,header: True
    >>> colnames = []
    >>> extract_rows(dummy, header, predicate, colnames) is None
    True

    >>> # `colnames` contains a non-column name
    >>> header = ['a', 'b', 'c']
    >>> dummy = [['a1', 'b1', 'c1'],['a2', 'b2', 'c2'],['a3', 'b3', 'c3']]
    >>> predicate = lambda row,header: True
    >>> colnames = ['a', 'd']
    >>> extract_rows(dummy, header, predicate, colnames) is None
    True

    >>> # Extract selected rows: whole rows returned
    >>> orig_hd = ['a', 'b', 'c']
    >>> orig_ds = [['a1', 'b1', 'c1'],['a2', 'b2', 'c2'],['a3', 'b3', 'c3']]
    >>> exp_hd = ['a', 'b', 'c']
    >>> exp_ds = [['a2', 'b2', 'c2'],['a3', 'b3', 'c3']]
    >>> predicate = lambda row, header: row[header.index('c')] > 'c1'
    >>> ret_ds, ret_hd = extract_rows(orig_ds, orig_hd, predicate)
    >>> ret_ds is not orig_ds and ret_ds == exp_ds and ret_hd is not orig_hd and ret_hd == exp_hd
    True

    >>> # Extract selected rows: columns 'a', and 'c', returned
    >>> orig_hd = ['a', 'b', 'c']
    >>> orig_ds = [['a1', 'b1', 'c1'],['a2', 'b2', 'c2'],['a3', 'b3', 'c3']]
    >>> exp_hd = ['a', 'c']
    >>> exp_ds = [['a2', 'c2'],['a3', 'c3']]
    >>> predicate = lambda row, header: row[header.index('c')] > 'c1'
    >>> ret_ds, ret_hd = extract_rows(orig_ds, orig_hd, predicate, ['a', 'c'])
    >>> ret_ds is not orig_ds and ret_ds == exp_ds and ret_hd is not orig_hd and ret_hd == exp_hd
    True
    """
    # Ensure valid `predicate`
    if type(predicate) is not type(lambda x,y: None) or \
       predicate.__code__.co_argcount != 2:
        return None
    # Extract row(s) meeting `predicate` conditions
    row_subset = []
    for row in dataset:
        if predicate(row, header):
            row_subset.append(row[:])
    # Return whole row set if no column names nominated
    if colnames is None:
        return row_subset, header[:]
    # Extract only nominated columns for each row
    if _is_valid_colnames(header, colnames):
        # Extract nominated columns
        columns_to_remove = [x for x in header if x not in set(colnames)]
        new_subset, new_header = \
            remove_columns(row_subset, header[:],
                           columns_to_remove,
                           inplace=True)
        return new_subset, new_header
    # Fallthrough case
    return None

if __name__ == "__main__":
    doctest.testmod()

