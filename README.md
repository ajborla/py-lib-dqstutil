# dqstutil - (d)ata (q)uery and (st)atistical (util)ities
> Simple table-based dataset query and management library

|||
| :---     | :--- |
| author:  | Anthony J. Borla |
| contact: | [ajborla@bigpond.com](ajborla@bigpond.com) |
| license: | MIT |

## Description
A collection of utility functions for querying and managing a table-based dataset, primarily
targeted for interactive use, either at the REPL, or with a Jupyter Notebook.

### Technologies
- Python 3.8+

### Features
- Simple to use, shallow learning curve
- No classes or frameworks, just a collection of functions
- No external dependancies

## Installation
This package is registered on the [Python Package Index (PyPI)](https://pypi.python.org)
as [dqstutil](https://pypi.python.org/pypi/dqstutil).

Direct installation may be accomplished via:

```sh
pip install dqstutil
```

Alternatively you may add the name, **dqstutil**, to your *requirements.txt* file, and
install it using:

```sh
pip install -r requirements.txt
```

## Usage
To access the library, perform the following:

```python
import dqstutil
```

For interactive access, it is suggested the following also be performed:

```python
from dqstutil import *
```

allowing function access without reference to its module.

A typical usage scenario would see a CSV file (with 1st row as column header) loaded:

```python
dataset, header = load_csv_dataset("data.csv")
```

The variables, `dataset` and `header`, would then refer to the data, and column names,
respectively, and be the chief arguments passed to invocations of the library functions.

For example, to extract all columns from a set of rows meeting some criterion:

```python
extraction_criterion = lambda ...
list_of_columns = [...]

subset_rows, subset_header = \
    extract_rows(dataset,
                 header,
                 extraction_criterion,
                 list_of_columns)
```

The [examples](https://github.com/ajborla/py-lib-dqstutil/examples/) area contains more detailed scenarios.

## Documentation
To get started quickly, refer to the [examples](https://github.com/ajborla/py-lib-dqstutil/examples/).

Details for how to use each function may then be obtained from the [API documentation](https://ajborla.github.io/py-lib-dqstutil/).
