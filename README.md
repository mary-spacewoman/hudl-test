# Hudl Login Test Suite
## Pre-requisites
This test suite requires a working installation of [Selenium](https://www.selenium.dev)
and its [Python bindings.](https://selenium-python.readthedocs.io)

[ChromeDriver](https://sites.google.com/chromium.org/driver/) binary should be available
in the `$PATH` variable.

You can use [Poetry](https://python-poetry.org) to install the necessary dependencies
using the provided lockfile.

## How to run
The environment variables `HUDL_TEST_EMAIL` and `HUDL_TEST_PASSWORD` must be set when
running the test suite, otherwise all the test cases will be skipped.

The test suite can be run from any environment with all the required dependencies as a
normal Python module:
```shell
python -m tests.test_hudl_login
```

Alternatively, with Poetry:
```
poetry run python -m tests.test_hudl_login
```

## Notes
This suite has been developed and run in the following environment:
* macOS 10.15.5
* Python 3.10.1
* Selenium 4.1.0
* ChromeDriver 97.0.4692.71


The `test_remember_me` test case currently doesn't work and unfortunately I haven't
been able to debug it.
There seems to be [evidence](https://stackoverflow.com/q/67126246) that the usual way of
saving sessions is broken in ChromeDriver 90.
