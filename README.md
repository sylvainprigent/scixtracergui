
# SciXtracerGui

GUI for the python implementation of the scientific experiment data management system called SciXtracer

# Documentation

The demo script ``demo.py`` shows a basic usage of the library

The documentation is available [here](https://sylvainprigent.github.io/scixtracer).

# Development

## Run tests

Test are written with unittest python package. All tests are located in the subpackage scixtracerpy/tests.
Run tests with the command:

```bash
cd scixtracerpy
pipenv run python -m unittest discover -v
```

## Build the documentation

The documentation is written with Sphinx. To build is run the commands:

```bash
cd docs
pipenv run sphinx-build -b html ./source ./build
```

