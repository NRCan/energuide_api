
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

## Tests


### Running tests locally
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

### Automated testing

This repo is connected to CircleCI, and all tests, linters, and static type checking must pass before merging to master.


## Running locally

For development purposes we can run the web apps on our local machine. 
First open four terminal windows:

**ETL**
```
cd nrcan_api/etl
make setup_python
source env/bin/activate
export ETL_SECRET_KEY=key
export EXTRACT_ENDPOINT_STORAGE_DOMAIN=http://127.0.0.1:10000/devstoreaccount1
export EXTRACT_ENDPOINT_STORAGE_ACCOUNT=devstoreaccount1
export EXTRACT_ENDPOINT_STORAGE_KEY=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==
export EXTRACT_ENDPOINT_CONTAINER=energuide-extracted-data
```

**Azure**
```
cd nrcan_api/extract_endpoint
mkdir -p tests/azure_emulator
azurite-blob -l tests/azure_emulator/data
```

**Endpoint**
```
cd nrcan_api/extract_endpoint
make setup_python
source env/bin/activate
export ETL_SECRET_KEY=key
export EXTRACT_ENDPOINT_STORAGE_DOMAIN=http://127.0.0.1:10000/devstoreaccount1
export EXTRACT_ENDPOINT_STORAGE_ACCOUNT=devstoreaccount1
export EXTRACT_ENDPOINT_STORAGE_KEY=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==
export EXTRACT_ENDPOINT_CONTAINER=energuide-extracted-data
python src/extract_endpoint/endpoint.py
```

**Endpoint Post**
```
cd nrcan_api/extract_endpoint
source env/bin/activate
export ETL_SECRET_KEY=key
```


The **Azure** terminal should display a message similar to
```
Azure Blob Storage Emulator listening on port 10000
```

while the **Endpoint** terminal should report
```
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
```

In the **ETL** window ensure that you have an empty Azure container:
```
az storage container delete --name energuide-extracted-data --connection-string 'DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;'
az storage container create --name energuide-extracted-data --connection-string 'DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;'
```
then run the extractor to create a Zip file:
```
energuide extract --infile tests/randomized_energuide_data.csv --outfile extract_out.zip
```
and finally start up the ETL web app
```
python src/energuide/flask_app.py
```
The app should report something similar to
```
2018-03-14T12:11:53-0400 - INFO - werkzeug:  * Running on http://0.0.0.0:5010/ (Press CTRL+C to quit)
```

We should have three apps running: Azure, the endpoint, and the ETL web app.

In the **Endpoint Post** terminal upload the extracted records (and a timestamp) via
```
extract_endpoint upload ../etl/extract_out.zip 2018-03-14
```

All terminals should produce output.

**Endpoint Post**

```
Response: 200, b''
```

**Endpoint**
```
127.0.0.1 - - [14/Mar/2018 12:18:30] "POST /upload_file HTTP/1.1" 200 -
```

**Azure**
```
...

GET /devstoreaccount1/energuide-extracted-data/55622-11W2D00606 206 2.107 ms - 260009
GET /blobs/nrzzoG8DH_bmt71vNYdM2CMUDYA= 206 0.719 ms - 260010
GET /devstoreaccount1/energuide-extracted-data/55622-11W2E00606 206 3.025 ms - 260010
```

**ETL**

```
...
2018-03-14T12:22:04-0400 - INFO - energuide.cli: Finished loading data
2018-03-14T12:22:04-0400 - INFO - __main__: Success, 7 created

```

You can also rerun the ETL app without uploading new files:
```
extract_endpoint run_tl
```

## Deploying

The two web apps `extract_endpoint/endpoint.py` and `energuide/flask_app.py`
run in Microsoft Azure.
To configure them to work correctly, both apps must have environment variables set pointing to the production Azure Storage.
* EXTRACT_ENDPOINT_STORAGE_DOMAIN
* EXTRACT_ENDPOINT_STORAGE_ACCOUNT
* EXTRACT_ENDPOINT_STORAGE_KEY
* EXTRACT_ENDPOINT_CONTAINER

The two apps and the local machine that will be running `extract_endpoint upload` must share a common environment
variable ETL_SECRET_KEY. This should be a random string of length at least 30 characters.

The `extract_endpoint/endpoint.py` app needs to have the environment variable TL_ADDRESS set to the url and port
of the `energuide/flask_app.py` app (by default the port is 5010). For example, 'https://0.0.0.0:5010'

The `energuide/flask_app.py` app must also have environment variables set pointing to the production Mongo database.
* ENERGUIDE_USERNAME
* ENERGUIDE_PASSWORD
* ENERGUIDE_HOST
* ENERGUIDE_PORT
* ENERGUIDE_DBNAME
* ENERGUIDE_COLLECTION

Finally, to upload files to production (or trigger the tl manually) we need to specify the url of the endpoint app
```
extract_endpoint upload ../etl/extract_out.zip 2018-03-14 --url=https://127.0.0.1:5000/upload_file
extract_endpoint run_tl --url=https://127.0.0.1:5000/upload_file
```
