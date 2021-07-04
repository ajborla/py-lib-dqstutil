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

## Development and Testing
### Source Code
The [dqstutil](https://github.com/ajborla/py-lib-dqstutil/) source is hosted on GitHub.
Clone the project with:

```sh
git clone https://github.com/ajborla/py-lib-dqstutil.git
```

### Tools
A comprehensive `Makefile` is included to facilitate develeopment and testing. For those
unfamiliar with the `make` utility, here is an easily digestible tutorial:
[What is a Makefile and how does it work?](https://opensource.com/article/18/8/what-how-makefile)

The `Makefile`:
- Attempts to be comprehensive, almost a 'one-stop shop' for development and testing the current project
- Breaks several `make` conventions (but then, this is a Python, not a C, project)
- Avoids the tab character trap (this relies on having a fairly recent `make` version)
- Styled more like a script than a typical `Makefile`

I sincerely hope I have not offended any `make` purists.

To use the `Makefile`:

```sh
make
```

and follow the instructions.

### Requirements
### Tests
### Documentation
Project documentation, specifically, the library API reference, resides in the `docs`
directory, and takes the form of:
- README.md, the documentation in Markdown form
- index.html, said README.md rendered as HTML, but styled as Markdown

Since the directory is published as a website, a `robots.txt` file also resides there.

Motivation for the dual provision (via .md and .html) of the documentation is so the same
information, in the same form, is readily available to both library end users and developers
accessing the repository.

Document generation is a two step process:
- Parse source code, converting docstrings to Markdown
- Convert Markdown to HTML

To perform the first step, a third-party Python utility, [doc2md](https://github.com/coldfix/doc2md)
 is used, whilst the second step is performed via a [nodejs](https://nodejs.org/en/)-based
third-party utility, [markdown-to-html-github-style](https://github.com/KrauseFx/markdown-to-html-github-style).

The actual conversion steps may be found in the document generation script, `docgen.sh`,
residing in the `docs` directory. It may be invoked directly, but is perhaps more conveniently
called from the `docs` target of the `Makefile`, an action performed via:

```sh
make docs
```

Note document generation only occurs if the source file timestamp has changed.

Some may find the reliance on third-party utilities (particularly those outside the
Python ecosystem) irksome. Possible alternatives/improvements:
- Use of more standard documentation generation tools such as [pydoc](https://docs.python.org/3/library/pydoc.html) or [Sphinx](https://www.sphinx-doc.org/en/master/)
- Custom Python conversion script

Candidates, certainly, for the [TODO](#todo) list!

### Examples

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

### TODO

## Contributing
Please submit and comment on bug reports and feature requests.

To submit a patch:

1. Fork it (https://github.com/ajborla/py-lib-dqstutil/fork).
2. Create your feature branch (`git checkout -b my-new-feature`).
3. Make changes. Write and run tests.
4. Commit your changes (`git commit -am 'Add some feature'`).
5. Push to the branch (`git push origin my-new-feature`).
6. Create a new Pull Request.

## License
This Python package is licensed under the MIT license.

## Warranty
This software is provided "as is" and without any express or implied
warranties, including, without limitation, the implied warranties of
merchantibility and fitness for a particular purpose.
