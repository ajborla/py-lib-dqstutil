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

## Meta
### Motivation
As part of ongoing professional development, I have been completing the learning tracks
at [Dataquest](https://www.dataquest.io/). While the curriculum includes use of Python
libraries like NumPy, Pandas, and Matplotlib in Jupyter Notebook-based projects, the first
few projects only make use of standard Python.

Rather than hard code the queries and transformations needed for these projects, I instead
assembled some helper functions with which to perform these tasks. I soon found that as I
worked on these notebook projects, an idea for a new function, or an expansion of an
existing one, would arise. It eventually occurred to me that packaging this functionality
as a Python package, in a form suitable for distribution on [PyPI](https://pypi.python.org),
would not only enhance my own learning experience, but also provide some utility to others
working on similar tasks.

### Acknowledgements
It is only fitting to acknowledge [Dataquest](https://www.dataquest.io/) since the project
would probably not have started without being inspired through my participation in this
curriculum.

Please note, however, inspiration aside, there is no connection between this project and
[Dataquest](https://www.dataquest.io/).

### Project Status
The project is active. However, since it was undertaken as a side project, and primarily as
part of a learning exercise, little further development is envisaged (but not ruled out). That
said, ideas, feedback, and contributions are welcome.
