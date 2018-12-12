# A Programmer's Introduction to Mathematics

[![travis-badge](https://travis-ci.org/pim-book/programmers-introduction-to-mathematics.svg?branch=master)](https://travis-ci.org/pim-book/programmers-introduction-to-mathematics) [![Coverage Status](https://coveralls.io/repos/github/pim-book/programmers-introduction-to-mathematics/badge.svg?branch=master)](https://coveralls.io/github/pim-book/programmers-introduction-to-mathematics?branch=master) [![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/pim-book/programmers-introduction-to-mathematics.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/pim-book/programmers-introduction-to-mathematics/context:python)

This repository contains the code implementing the applications from each
chapter of [A Programmer's Introduction to Mathematics](https://pimbook.org).
All code is written in Python 3.x. Feel free to submit a pull request if you
find a bug.

To install the requirements and run the examples, using pip and virtualenv (Python's standard packaging tools):

```
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
```

To run the test suite:

```
pytest

# with code coverage
pytest --cov-report html:cov_html  --cov-report annotate:cov_annotate --cov
```
