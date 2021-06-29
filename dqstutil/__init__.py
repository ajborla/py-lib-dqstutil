"""
**Simple table-based dataset query and management library**.

Collection of utility functions for querying and managing a
table-based dataset.

This package is registered on the Python Package Index (PyPI) at
[pypi.python.org/pypi/dqstutil](https://pypi.python.org/pypi/dqstutil).

The source is hosted on GitHub at
[github.com/ajborla/py-lib-dqstutil](https://github.com/ajborla/py-lib-dqstutil).

Library API reference is available at
[ajborla.github.io/py-lib-dqstutil](https://ajborla.github.io/py-lib-dqstutil).

Please see the README at either location above for more details about
this package.
"""


from .version import __version__

from .dqstutil import \
    _is_valid_colnames, is_numeric, is_possible_date, \
    is_possible_numeric, determine_column_type, \
    inspect_dataset, gen_unique_values_count, \
    extract_unique_values, _extract_unique_values, \
    gen_freq_table, load_csv_dataset, add_column, \
    remove_column, modify_column, transform_column, \
    remove_columns, extract_row_range, extract_rows

__all__ = [
    '_is_valid_colnames',
    'is_numeric',
    'is_possible_date',
    'is_possible_numeric',
    'determine_column_type',
    'inspect_dataset',
    'gen_unique_values_count',
    'extract_unique_values',
    '_extract_unique_values',
    'gen_freq_table',
    'load_csv_dataset',
    'add_column',
    'remove_column',
    'modify_column',
    'transform_column',
    'remove_columns',
    'extract_row_range',
    'extract_rows'
]
