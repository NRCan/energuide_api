# Energuide API - Extract to endpoint component

This component takes the output files from the extract process and posts them to an endpoint which then uploads them to
Azure for use by the transform process.

## Installation

### Python 3.6
Energuide API - Extract to endpoint is tested to run on Python 3.6. To begin, you will need to have Python 3.6
installed.

We recommend `pyenv` as an easy way to easily install and switch between any versions of Python that you need.

See https://github.com/pyenv/pyenv#installation for pyenv installation instructions.

If you're running macOS, you can use the [bootstrap.sh](https://github.com/cds-snc/nrcan_api#bootstrapsh) file to
install Python 3.6 via Homebrew. On Windows, you can download and install Python from
[here](https://www.python.org/downloads/release/python-364/). Please make sure to install version 3.6.4 or higher.

### Azure emulator
In order to run and test the endpoint locally, you will need to install and run an Azure emulator. Before attempting to
run the project or tests locally you will need to make sure the emulator is running.

#### On macOS:

```
# install via NPM, requires Node to be installed
npm install -g azurite

# create directory to store emulator data
mkdir -p tests/azure_emulator

# run emulator
azurite-blob -l tests/azure_emulator/data
```

#### On Windows:
Download and install the emulator from [here](https://docs.microsoft.com/en-us/azure/storage/common/storage-use-emulator).

### Virtualenv
Installing Python applications in a `virtualenv` is considered best practice.

#### On macOS:

```
python3 -m venv env
source env/bin/activate
```

#### On Windows:

```
python -m venv env
env\Scripts\activate.bat
```
This will create a new virtualenv in a  folder called `env`, and activate the virutalenv. To deactivate the virtualenv, run `deactivate`

#### Installing the app

Inside an activated virtualenv, and from the python folder of the project, run:
```
pip install -r requirements.txt
pip install -e .
```

#### Running the app


#### Running tests locally
Many of the tests require an Azure emulator running locally. Please refer to the [Azure](#azure-emulator) section for more information on how to download
and run an emulator.

To run the tests, run:
```
pytest tests
```

To run the linter, run:
```
pylint src tests
```

To run the mypy type checker, run:
```
mypy src tests --ignore-missing-imports
```

#### Automated Testing

This repo is connected to CircleCI, and all tests, linters, and static type checking must pass before merging to master.

