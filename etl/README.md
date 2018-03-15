## Energuide API - ETL component

### Installation

#### Python 3.6

Energuide API - ETL is tested to run on Python 3.6. To begin, you will need to have Python 3.6 installed.

We recommend `pyenv` as an easy way to easily install and switch between any versions of Python that you need.

See https://github.com/pyenv/pyenv#installation for pyenv installation instructions.

#### MongoDB

To run the ETL, you need to be able to access a MongoDB instance. For instructions on installing one locally, see https://docs.mongodb.com/manual/administration/install-community/

#### Virtualenv

Installing Python applications in a `virtualenv` is considered best practice. To do so, run:
```
python3 -m venv env
source env/bin/activate
```
This will create a new virtualenv in a  folder called `env`, and activate the virutalenv. To deactivate the virtualenv, run `deactivate`

**WINDOWS NOTE** To activate a virtual environment on Windows instead run `env\Scripts\activate.bat`

#### Installing the app

Inside an activated virtualenv, and from the python folder of the project, run:
```
pip install -r requirements.txt
pip install -e .
```

#### Running the app

The ETL application is accessed from the `energuide` CLI. Run `energuide --help` for help.

There are currently two commands for energuide:
```
energuide extract --infile /path/to/file --outfile /path/to/other/file
```

```
energuide load --filename /path/to/file
```

These two commands are meant to be chained together,`energuide load` accepts a file that is output by `energuide extract`.

A sample file is included for demonstration purposes at `./tests/randomized_energuide_data.csv`

By default, the `energuide load` command connects using the following defaults:
- username: `''` (blank)
- password: `''` (blank)
- host: `localhost`
- port: `27017`
- database: `energuide`
- collection: `dwellings`

Any of these defaults may be overridden at the command line using command-line flags:
```
energuide load --username my_username --filename path/to/file
```
They may also be overriden using environment variables prefixed with `ENERGUIDE_`:
```
ENERGUIDE_USERNAME=my_username energuide load --filename path/to/file
```

Run `energuide load --help` for a full list of available options.

#### Running tests locally

Many of the tests require a running local MongoDB server. It will attempt to connect using the environment variable values, if they are set, or the defaults if they are not.

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
mypy src tests
```

#### Automated Testing

This repo is connected to CircleCI, and all tests, linters, and static type checking must pass before merging to master.


### Running Locally

The system can be run locally using the CLI commands that are described above, but to run all the components behaving as they do when deployed to Azure, follow instructions in the **Running Locally** section of the `extract_endpoint` module.
