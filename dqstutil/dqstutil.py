"""
Collection of utility functions for managing a dataset.

A dataset comprises an ordered collection of rows, with each row
having an equal number of columns. It may be considered a rectangular
structure, similar to a spreadsheet.
"""


def _is_valid_colnames(header, colnames):
    """
    Validate column names against header.

    Given a list of column name, `colnames`, returns True if each
    element is also in the list, `header`.

    :param header: list
    :param colnames: list

    :return: bool
    """
    return \
        isinstance(header, list) \
        and len(header) > 0 \
        and isinstance(colnames, list) \
        and len(colnames) > 0 \
        and all(map(lambda x: x in header, colnames))


def is_numeric(numstr):
    """
    Check string for numeric convertability.

    Given `numstr`, returns True if it is either a numeric type, or a
    numeric-convertible string.

    :param numstr: str

    :return: bool
    """
    def to_complex():
        try:
            complex(numstr)
            return True
        except ValueError:
            return False

    if not isinstance(numstr, str):
        return type(numstr) in [int, float, complex]

    return \
        numstr.isnumeric() \
        or to_complex()


def is_possible_date(datestr):
    """
    Check string for possible date-format conformance.

    Given `datestr`, returns True if it is possibly a date-convertible
    string.

    :param datestr: str

    :return: bool
    """
    month_prefixes = [
        'jan', 'feb', 'mar', 'apr',
        'may', 'jun', 'jul', 'aug',
        'sep', 'oct', 'nov', 'dec'
    ]

    def is_date_separator(char):
        return char in ['/', '-']
    # Lowercase `datestr` to simplify character comparisons
    datestr = datestr.lower()
    # Valid candidate must contain a month name or exactly two
    # date separator characters
    return \
        any(map(lambda month: month in datestr, month_prefixes)) \
        or len(list(filter(is_date_separator, datestr))) == 2


def is_possible_numeric(numstr):
    """
    Check string for possible numeric-format conformance.

    Given `numstr`, returns True if it is possibly a numeric-convertible
    string, such as a currency value or comma-separted numeric, or a
    suffixed value (such as a measurement). Note that version strings
    (often having two or more decimal points) are NOT considered
    possible numerics.

    :param numstr: str

    :return: bool
    """
    # Tests for string `s` numeric-format compliance
    contains_one_or_more_digits = \
        any(map(lambda char: char.isdigit(), numstr))
    contains_zero_or_one_decimal_point = \
        len(list(filter(lambda char: char == '.', numstr))) < 2
    contains_zero_or_one_dollar_sign = \
        len(list(filter(lambda char: char == '$', numstr))) < 2
    is_not_possible_date = \
        not is_possible_date(numstr)
    # Apply tests, return result
    return \
        contains_one_or_more_digits \
        and is_not_possible_date \
        and contains_zero_or_one_decimal_point \
        and contains_zero_or_one_dollar_sign


def determine_column_type(coldata):
    """
    Determine a column's possible datatype.

    Given `coldata`, returns string indicating its possible type,
    one of:

        T  - text
        N  - numeric (safely convertible to)
        PD - possibly a date
        PN - possibly a numeric

    :param coldata: str

    :return: str
    """
    if is_numeric(coldata):
        return 'N'
    if is_possible_numeric(coldata):
        return 'PN'
    if is_possible_date(coldata):
        return 'PD'
    return 'T'


def inspect_dataset(dataset, header, generate_report=True,
                    printer=print):
    """
    Extract metadata, and either return it, or print it.

    Given `dataset` and `header`, inspects `dataset` collecting
    metadata, and either returns metadata or generates, and prints,
    a report. By default, data is printed using the built-in `print`
    function, but allows an alternate function (such as `pprint`) to
    be used via the `printer` argument.

    `dataset` is a list of lists, each sublist a 'row' in the
    dataset, `header` is a list of strings, each identifying a
    corresponding 'column' in the dataset. The metadata collected
    includes:
        skiprows, a list of non length-conformant row numbers
        columns, a dict, keyed by column name, each containing a
          dict of column-type-identifying codes (see the function,
          'determine_column_type' for details)
        uniques, a dict, keyed by column name, each containing the
          count of unique values in text-only-type columns

    :param dataset: list
    :param header: list
    :param generate_report: bool
    :param printer: function

    :return: None|tuple(list, dict, dict)
    """
    # 1. Column metadata repository keyed using column headers
    columns = {}
    for colname in header:
        columns[colname] = {}
    # a. Collect non length-conformant row numbers
    skiprows = []
    rowlen = len(header)
    for rowidx, row in enumerate(dataset):
        # Check for row length conformance
        if len(row) != rowlen:
            skiprows.append(rowidx)
    # b. Collect column type data
    for rowidx, row in enumerate(dataset):
        # Skip non length-conformant rows
        if rowidx in skiprows:
            continue
        # Check column type conformance
        for colname, colval in zip(header, row):
            coltype = determine_column_type(colval)
            if coltype in columns[colname]:
                columns[colname][coltype] += 1
            else:
                columns[colname][coltype] = 1
    # c. Collect unique values data
    uniques = {}
    for colname in header:
        uniques[colname] = {'N': [], 'PD': [], 'PN': [], 'T': []}
    for rowidx, row in enumerate(dataset):
        # Skip non length-conformant rows
        if rowidx in skiprows:
            continue
        # Collect unique values for all column types
        for colname, colval in zip(header, row):
            coltype = determine_column_type(colval)
            if colval not in uniques[colname][coltype]:
                uniques[colname][coltype].append(colval)
    # Replace collect unique values with their count
    for colname in header:
        for coltype in ['N', 'PD', 'PN', 'T']:
            uqcollen = len(uniques[colname][coltype])
            # Remove entries with zero unique count
            if uqcollen < 1:
                del uniques[colname][coltype]
            else:
                uniques[colname][coltype] = uqcollen
    # 2. Either generate report if requested, or return collected values
    if generate_report:
        row_rep_header = \
            'Invalid (incorrect length) row numbers:'
        col_rep_header = \
            'Tentative column type(s) [T - text, N - numeric,' \
            ' PN - possible numeric, PD - possible date]:'
        unique_rep_header = \
            'Unique value counts for each column type:'
        print(row_rep_header, end='')
        printer(skiprows)
        print('', col_rep_header, '', sep='\n')
        printer(columns)
        print('', unique_rep_header, '', sep='\n')
        printer(uniques)
        # To signal no values returned
        return None
    # Return collected metadata as tuple
    return skiprows, columns, uniques


def gen_unique_values_count(dataset, header, colname):
    """
    Generate unique values count of a single dataset column.

    Given  a `dataset`, its `header`, and a column name, `colname`,
    categorises column contents into one of four categories, and
    returns a table (dict) of category counts.

    :param dataset: list
    :param header: list
    :param colname: str

    :return: dict|None
    """
    if isinstance(colname, str) and colname in header:
        # Collect unique values data
        unique = {'N': [], 'PD': [], 'PN': [], 'T': []}
        colidx = header.index(colname)
        for row in dataset:
            colval = row[colidx]
            coltype = determine_column_type(colval)
            if colval not in unique[coltype]:
                unique[coltype].append(colval)
        for coltype in ['N', 'PD', 'PN', 'T']:
            uqcollen = len(unique[coltype])
            unique[coltype] = uqcollen
            # Remove entries with zero unique count
            if uqcollen < 1:
                del unique[coltype]
        return unique
    # Fallthrough case
    return None


def extract_unique_values(dataset, header, colname, coltype='T',
                          sort=False):
    """
    Extract unique values, of a specific type, from a single
    dataset column.

    Given  a `dataset`, its `header`, a column name, `colname`,
    and `coltype`, one of 'N' (numeric), 'PN' (possible numeric),
    'PD' (possible date), or 'T' (text), returns the unique values
    of the nominated `coltype` (defaults to 'T'), optionally
    sorted, ascending.

    :param dataset: list
    :param header: list
    :param colname: str
    :param coltype: str
    :param sort: bool

    :return: list|None
    """
    if isinstance(colname, str) and colname in header:
        # Extract the column from the dataset
        coldata = []
        colidx = header.index(colname)
        for row in dataset:
            colval = row[colidx]
            if coltype == determine_column_type(colval):
                coldata.append(colval)
        # Extract list of the column's unique values
        return _extract_unique_values(coldata, sort)
    # Fallthrough case
    return None


def _extract_unique_values(values, sort=False, sep='|'):
    """
    Extract unique values from a list of values.

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

    :return: list|None
    """
    # Exclude obvious non-candidates
    if not isinstance(values, list) or len(values) < 1:
        return None
    # Ensure homogeneity of list elements
    value_type = type(values[0])
    if not all(map(lambda value: isinstance(value, value_type), values)):
        return None
    # Select algorithm based on element type: list or other
    if value_type is list:
        value_len = len(values[0])
        # Ensure all sublists are non-empty, have identical length,
        # and do not, themselves, contain lists
        if value_len == 0:
            return None

        def contains_no_list(value):
            return all(map(lambda x: not isinstance(x, list), value))

        def is_homogenous(value, template):
            return all(map(lambda x: type(x) is type(template), value))

        if not all(map(lambda value: len(value) == value_len
           and contains_no_list(value)
           and is_homogenous(value, value[0]), values)):
            return None
        # Return values depend on sublist element number
        if value_len > 1:
            # Unique values returned as string, concatenation of
            # individual values

            def to_str(value):
                return \
                    map(lambda x: x if isinstance(x, str) else str(x),
                        value)

            uniques = \
                [sep.join(to_str(value))
                    for value in set([tuple(value) for value in values])]
        else:
            # Unique values returned as original type
            uniques = \
                [value[0] for value in
                    set([tuple(value) for value in values])]
    else:
        # Non-list element type; unique values returned as original
        # type
        uniques = \
            [value for idx, value in
                enumerate(values) if value not in values[:idx]]
    # Sorted (ascending) unique value list, if requested
    return sorted(uniques) if sort else uniques


def gen_freq_table(dataset, header, colname, sort_by_value=False,
                   reverse=False):
    """
    Generate a table of frequency counts and relative percetages.

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
        for meta in freq_table.values():
            meta[1] = (meta[0] / total_rows) * 100
            meta = tuple(meta)
        # Sort table
        if sort_by_value:
            return dict(sorted(freq_table.items(),
                               key=lambda item: item[1][0],
                               reverse=reverse))
        return dict(sorted(freq_table.items(),
                           key=lambda item: item[0],
                           reverse=reverse))
    # Fallthrough case
    return None


def load_csv_dataset(filename, sep=',', encoding='utf8'):
    """
    Load into dataset, data from a comma-separated value (CSV) file.

    Given `filename`, the name of a CSV file, that is expected to
    be encoded with `encoding`, and datums separated with `sep`,
    loads contents as a list of lists. The dataset is therefore
    implemented as a list containing a number of sublists, each of
    which represents a row of data, and each corresponding element
    of these rows considered to be part of a column.

    It is expected the first row of the CSV file to be a list of
    column names.

    :param filename: str
    :param sep: str
    :param encoding: str

    :return: list, list|None, None
    """
    from os.path import exists as file_exists
    from csv import reader as csv_reader
    if isinstance(filename, str) and len(filename) > 0 \
       and file_exists(filename):
        with open(filename, encoding=encoding) as csvdata:
            data = list(csv_reader(csvdata, delimiter=sep))
            header, dataset = data[0], data[1:]
        return dataset, header
    # Fallthrough case
    return None, None


def add_column(dataset, header, colname, coldata, inplace=False):
    """
    Add a new column to a dataset.

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
    """
    if isinstance(colname, str) and len(colname) > 0 \
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
    Remove a nominated column from a dataset.

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
    """
    if isinstance(colname, str) and colname in header:
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
    return None, None


def modify_column(dataset, header, colname, coldata, inplace=False):
    """
    Modify all data within the nominated column of a dataset.

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
    """
    if isinstance(colname, str) and len(colname) > 0 \
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
    Apply a transform function to the nominated column of a dataset.

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
    """
    if isinstance(colname, str) \
       and len(colname) > 0 \
       and colname in header \
       and callable(transform):
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
    Remove a set of columns from a dataset.

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
    return None, None


def extract_row_range(dataset, rowrange):
    """
    Extract a set of range-defined rows from a dataset.

    Given  a `dataset`, and a `rowrange` (a two-element tuple|list
    containing integers), extracts, and returns, from `dataset`,
    the set of rows numbered from `rowrange[0]` through `rowrange[1`,
    inclusive. Note row numbering is from 0 through len(dataset)-1.

    :param dataset: list
    :param rowrange: list

    :return: None|list
    """
    lower_bound, upper_bound = rowrange
    if lower_bound < 0 or lower_bound > upper_bound:
        return None
    if upper_bound < lower_bound or upper_bound > len(dataset)-1:
        return None
    if lower_bound != upper_bound:
        return dataset[lower_bound:(upper_bound+1)]
    return [dataset[lower_bound]]


def extract_rows(dataset, header, sieve=None, colnames=None):
    """
    Extract either all rows, or a subset of rows meeting a
    sieve condition, from a dataset.

    Given  a `dataset`, its `header`, and, optionally, a 2-argument
    function, `sieve`, and (also optionally) a list of column names,
    `colnames`, applies the sieve to each row of the dataset, and
    retains the row if the sieve condition returns True.

    If `colnames` is supplied, keeps the nominated columns from the
    retained rows, discarding all others. A copy of the header is
    updated to reflect these changes. In all cases copies of the dataset
    and header (whether modified or not) are returned (there is no
    'inplace' modification).

    If no sieve is supplied, all rows are returned, otherwise, for
    each row of the dataset, `sieve` receives the row, as well as
    `header`. `sieve` uses the arguments to craft a boolean expression
    that returns True if the row is to be retained. Example sieve
    implementations:

      `lambda row, header: row[header.index('c')] > 'c1'`
      `def sieve(row, header): return row[header.index('c')] > 'c1'`

    :param dataset: list
    :param header: list
    :param sieve: function
    :param colnames: None|ist

    :return: list, list
    """
    # Check for no `sieve`, so whole dataset processed
    if sieve is None:
        row_subset = dataset[:]
    else:
        # Ensure valid `sieve` passed since sieveing requested
        if not callable(sieve) \
           or sieve.__code__.co_argcount != 2:
            return None
        # Extract row(s) meeting `sieve` conditions
        row_subset = []
        for row in dataset:
            if sieve(row, header):
                row_subset.append(row[:])
    # Return whole row set if no column names nominated
    if colnames is None:
        return row_subset, header[:]
    # Extract only nominated columns for each row
    if _is_valid_colnames(header, colnames):
        # Extract nominated columns
        columns_to_remove = \
            [x for x in header if x not in set(colnames)]
        new_subset, new_header = \
            remove_columns(row_subset, header[:],
                           columns_to_remove,
                           inplace=False)
        return new_subset, new_header
    # Fallthrough case
    return None


if __name__ == "__main__":
    pass
