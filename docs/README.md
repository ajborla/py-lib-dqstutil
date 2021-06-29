# dqstutil - (d)ata (q)uery and (st)atistical (util)ities

**Simple table-based dataset query and management**.

- [API](#api)
    - [_is_valid_colnames](#_is_valid_colnames)
    - [is_numeric](#is_numeric)
    - [is_possible_date](#is_possible_date)
    - [is_possible_numeric](#is_possible_numeric)
    - [determine_column_type](#determine_column_type)
    - [inspect_dataset](#inspect_dataset)
    - [gen_unique_values_count](#gen_unique_values_count)
    - [extract_unique_values](#extract_unique_values)
    - [_extract_unique_values](#_extract_unique_values)
    - [gen_freq_table](#gen_freq_table)
    - [load_csv_dataset](#load_csv_dataset)
    - [add_column](#add_column)
    - [remove_column](#remove_column)
    - [modify_column](#modify_column)
    - [transform_column](#transform_column)
    - [remove_columns](#remove_columns)
    - [extract_row_range](#extract_row_range)
    - [extract_rows](#extract_rows)

Collection of utility functions for querying and managing a
table-based dataset.

This package is registered on the Python Package Index (PyPI) at
[pypi.python.org/pypi/dqstutil](https://pypi.python.org/pypi/dqstutil).

The source is hosted on GitHub at
[github.com/ajborla/py-lib-dqstutil](https://github.com/ajborla/py-lib-dqstutil).

Please see the README at either location above for more details about
this package.


## API

- [_is_valid_colnames](#_is_valid_colnames)
- [is_numeric](#is_numeric)
- [is_possible_date](#is_possible_date)
- [is_possible_numeric](#is_possible_numeric)
- [determine_column_type](#determine_column_type)
- [inspect_dataset](#inspect_dataset)
- [gen_unique_values_count](#gen_unique_values_count)
- [extract_unique_values](#extract_unique_values)
- [_extract_unique_values](#_extract_unique_values)
- [gen_freq_table](#gen_freq_table)
- [load_csv_dataset](#load_csv_dataset)
- [add_column](#add_column)
- [remove_column](#remove_column)
- [modify_column](#modify_column)
- [transform_column](#transform_column)
- [remove_columns](#remove_columns)
- [extract_row_range](#extract_row_range)
- [extract_rows](#extract_rows)


## _is_valid_colnames

Validate column names against header.


Given a list of column name, `colnames`, returns True if each
element is also in the list, `header`.

:param header: list<br>
:param colnames: list

:return: bool


## is_numeric

Check string for numeric convertability.


Given `numstr`, returns True if it is either a numeric type, or a
numeric-convertible string.

:param numstr: str

:return: bool


## is_possible_date

Check string for possible date-format conformance.


Given `datestr`, returns True if it is possibly a date-convertible
string.

:param datestr: str

:return: bool


## is_possible_numeric

Check string for possible numeric-format conformance.


Given `numstr`, returns True if it is possibly a numeric-convertible
string, such as a currency value or comma-separated numeric, or a
suffixed value (such as a measurement). Note that version strings
(often having two or more decimal points) are NOT considered
possible numerics.

:param numstr: str

:return: bool


## determine_column_type

Determine a column's possible datatype.


Given `coldata`, returns string indicating its possible type,
one of:

    T  - text
    N  - numeric (safely convertible to)
    PD - possibly a date
    PN - possibly a numeric

:param coldata: str

:return: str


## inspect_dataset

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

:param dataset: list<br>
:param header: list<br>
:param generate_report: bool<br>
:param printer: function

:return: None|tuple(list, dict, dict)


## gen_unique_values_count

Generate unique values count of a single dataset column.


Given  a `dataset`, its `header`, and a column name, `colname`,
categorises column contents into one of four categories, and
returns a table (dict) of category counts.

:param dataset: list<br>
:param header: list<br>
:param colname: str

:return: dict|None


## extract_unique_values

Extract unique values, of a specific type, from a single dataset column.


Given  a `dataset`, its `header`, a column name, `colname`,
and `coltype`, one of 'N' (numeric), 'PN' (possible numeric),
'PD' (possible date), or 'T' (text), returns the unique values
of the nominated `coltype` (defaults to 'T'), optionally
sorted, ascending.

:param dataset: list<br>
:param header: list<br>
:param colname: str<br>
:param coltype: str<br>
:param sort: bool

:return: list|None


## _extract_unique_values

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

:param values: list<br>
:param sort: bool<br>
:param sep: str

:return: list|None


## gen_freq_table

Generate a table of frequency counts and relative percetages.


Given  a `dataset`, its `header`, a column name, `colname`,
generates a frequency table keyed by `colname`, and including both
the count and relative percentage as a tuple. Returned table is
sorted by key, that is, by `colname`, ascending. The value of
optional boolean arguments, `sort_by_value` and `reverse`,
determine alternate ordering of the table entries.

:param dataset: list<br>
:param header: list<br>
:param colname: str<br>
:param sort_by_value: bool<br>
:param reverse: bool

:return: dict


## load_csv_dataset

Load into dataset, data from a comma-separated value (CSV) file.


Given `filename`, the name of a CSV file, that is expected to
be encoded with `encoding`, and datums separated with `sep`,
loads contents as a list of lists. The dataset is therefore
implemented as a list containing a number of sublists, each of
which represents a row of data, and each corresponding element
of these rows considered to be part of a column.

It is expected the first row of the CSV file to be a list of
column names.

:param filename: str<br>
:param sep: str<br>
:param encoding: str

:return: list, list|None, None


## add_column

Add a new column to a dataset.


Given  a `dataset`, its `header`, and a single column name,
`colname`, and a list of data, `coldata` with an element for
each row in `dataset`, adds `colname` to the dataset and fills
it with the data from `coldata`. A copy of the dataset, and
header is modified unless `inplace` is True, in which case,
the original dataset and original header, with modifications,
are returned. Note dataset copy is a copy of the container and
copies of the elements too.

:param dataset: list<br>
:param header: list<br>
:param colname: str<br>
:param coldata: list<br>
:param inplace: bool

:return: list, list|None, None


## remove_column

Remove a nominated column from a dataset.


Given  a `dataset`, its `header`, and a single column name,
`colname`, removes the nominated column from `dataset` and
from the `header`. A copy of the dataset, and of the header,
is modified and returned, unless `inplace` is True, in
which case, the original dataset and original header, with
modifications, are returned. Note dataset copy is a copy of
the container and copies of the elements too.

:param dataset: list<br>
:param header: list<br>
:param colname: str<br>
:param inplace: bool

:return: list, list|None, None


## modify_column

Modify all data within the nominated column of a dataset.


Given  a `dataset`, its `header`, and a single column name,
`colname`, and a list of data, `coldata` with an element for
each row in `dataset`, replaces the data in the column,
`colname` with the data from `coldata`. A copy of the dataset,
is modified unless `inplace` is True, in which case, the
original dataset, with modifications, and the original header,
are returned. Note dataset copy is a copy of the container and
copies of the elements too.

:param dataset: list<br>
:param header: list<br>
:param colname: str<br>
:param coldata: list<br>
:param inplace: bool

:return: list, list|None, None


## transform_column

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

    lambda c: c.lower()
    def transform(c): return c.lower()

    lambda c, r, h: c + r[h.index('c2')]
    def transform(c, r, h): return c + r[h.index('c2')]

:param dataset: list<br>
:param header: list<br>
:param colname: str<br>
:param transform: function<br>
:param inplace: bool

:return: list, list|None, None


## remove_columns

Remove a set of columns from a dataset.


Given a `dataset`, its `header`, and a list of column names,
`colnames`, removes the nominated columns from `dataset` and
from the `header`. A copy of the dataset, and of the header,
is modified and returned, unless `inplace` is True, in
which case, the original dataset and original header, with
modifications, are returned. Note dataset copy is a copy of
the container and copies of the elements too.

:param dataset: list<br>
:param header: list<br>
:param colnames: list<br>
:param inplace: bool

:return: list, list|None, None


## extract_row_range

Extract a set of range-defined rows from a dataset.


Given  a `dataset`, and a `rowrange` (a two-element tuple|list
containing integers), extracts, and returns, from `dataset`,
the set of rows numbered from `rowrange[0]` through `rowrange[1`,
inclusive. Note row numbering is from 0 through len(dataset)-1.

:param dataset: list<br>
:param rowrange: list

:return: None|list


## extract_rows

Extract either all rows, or a subset of rows meeting a sieve condition,     from a dataset.


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

    lambda row, header: row[header.index('c')] > 'c1'

    def sieve(row, header): return row[header.index('c')] > 'c1'

:param dataset: list<br>
:param header: list<br>
:param sieve: function<br>
:param colnames: None|list

:return: list, list
