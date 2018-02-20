# NRCAN's Energuide API

CircleCI Status: [![CircleCI](https://circleci.com/gh/cds-snc/nrcan_api.svg?style=svg)](https://circleci.com/gh/cds-snc/nrcan_api)

This is the API for NRCAN's Energuide data.

This project is composed of two parts: the API itself and the ETL process that produces the data the API will serve.
There are further details in the READMEs for each of the respective portions of the project.

- [Windows Installation Instructions](#windows-installation)
- [MacOS Installation Instructions](#tldr)

## Quickstart

### TL;DR

If you're really keen (and on a Mac), this should do you. Or continue reading for more details.

```sh
# install python 3 and mongo
./bootstrap.sh

# import data
make setup

# export Apollo Engine API Key
export NRCAN_ENGINE_API_KEY=your_api_key

# boot up API
make run
```

### bootstrap.sh

The [bootstrap.sh]() file is a quick way to get up-and-running on a macOS environment. It relies on [Homebrew](https://brew.sh/) to install both Python 3 (using [pyenv](https://github.com/pyenv/pyenv#homebrew-on-mac-os-x)) and [MongoDB](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-os-x/#install-mongodb-community-edition-with-homebrew).

To get started, run

```
./bootstrap.sh
```

*Note that to get pyenv running by default in your preferred shell, you'll need to add `eval "$(pyenv init -)"` to your `~/.bash_profile` or `~/.zshrc` or after installing pyenv.*

Once the script runs through, you'll need to import the data into your database, and then boot up the API that connects to it.

#### importing data

The Python code in `/etl` transforms the data from the default formatting set by NRCAN, and then inserts it into our Mongo database. More details can be found in the [README](https://github.com/cds-snc/nrcan_api/blob/master/etl/README.md).

For local development, run
```
make setup
```
This will
- install the needed Python dependencies
- drop your current test data (if you have any)
- import fresh test data

Now that we have data, it's time to boot up the API.

#### running the API

##### Getting an Apollo Engine API Key

Apollo Engine is a monitoring/logging layer that gives us out-of-the-box diagnostic information about our graphql instance. You'll need your own API key to get the API running, so [sign up for one here](https://engine.apollographql.com/login).

Once you have one, you'll need to
```
export NRCAN_ENGINE_API_KEY=your_api_key
```


##### booting up the API

The JavaScript code in `/api` builds us a [GraphQL](http://graphql.org/learn/) API which allows us to query NRCAN data from the Mongo database. More info in the [README](https://github.com/cds-snc/nrcan_api/blob/master/api/README.md).

To build the app and connect it to mongo, run
```
make watch
```

This will
- install the needed JavaScript dependencies
- build the app
- serve it up locally
- rebuild when files are changed

## Windows installation

### Install required software

1. Download and install Python from [here](https://www.python.org/downloads/release/python-364/).
Version 3.6.4 or higher is required.

2. Download current version of mongoDB community server from [here](https://www.mongodb.com/download-center#community).

3. Download Node.js from [here](https://nodejs.org/en/download/). Version >=8.x of Node is required.

Check if the libraries are accessible by running the following commands in a terminal window
```sh
python --version

mongo --version

node --version
```
If version is not shown, the path to the library has to be added to the 'PATH' environment variable in System Properties.

NOTE: If you're having problems, make sure that you are not adding the library to a different user's 'PATH' (such as the user path of the local admin). The library can be added to the System 'PATH' variable so that it is visible to all users on the machine.
![System 'PATH' is highlighted](https://raw.githubusercontent.com/cds-snc/nrcan_api/master/resource/system_path.png)

### Run python extractor

Installing Python applications in a `virtualenv` is considered best practice. To do so, run:
```sh
cd \etl
python -m venv env
env\Scripts\activate.bat
```
Inside an activated `virtualenv`, and from the etl folder of the project, run:

```sh
pip install -r requirements.txt
pip install -e .
```
*Note: "." is part of the command*

`Mongodb` must be started before going to the next step. Open new terminal window and type
```sh
# this directory is required when running mongod for the first time
md \data\db
mongod
```
Keep this window open to continue running the database and open a new one to finish extracting the data.

Finish python part of installation.

Run the following command drop existing `energuide mongodb` test data.
```
mongo energuide --eval "db.dwellings.drop()"
```

Run the following python commands:
```sh
# extract from csv to zip file
energuide extract --infile tests/randomized_energuide_data.csv --outfile allthedata.zip

# load data into mongodb
energuide load --filename allthedata.zip

# delete zip file
del allthedata.zip
```
Unit tests for the python code.
```sh
pytest tests
mypy src tests --ignore-missing-imports
```

#### using the mongodb command-line client
We can verify the data has actually been imported by using the mongodb command-line client. [More detailed docs exist](https://docs.mongodb.com/manual/reference/mongo-shell/), but these should get you going.

Run following command to connect to `energuide`db:
```sh
#open db client
mongo

# show available databases ('energuide' should exist)
show dbs

# set energuide as the default 'db'
use energuide

# get the count of entries in 'dwellings' (should be 7)
db.dwellings.count()

# select 'forwardSortationArea' value of each dwelling
db.dwellings.find({}, {'forwardSortationArea': 1})

# result should  look like:
{ "_id" : ObjectId("5a848002e349de06d4bc8205"), "forwardSortationArea" : "T0J" }
{ "_id" : ObjectId("5a848002e349de06d4bc8206"), "forwardSortationArea" : "A2H" }
{ "_id" : ObjectId("5a848002e349de06d4bc8207"), "forwardSortationArea" : "Y1A" }
{ "_id" : ObjectId("5a848002e349de06d4bc8208"), "forwardSortationArea" : "G1A" }
{ "_id" : ObjectId("5a848002e349de06d4bc8209"), "forwardSortationArea" : "B2R" }
{ "_id" : ObjectId("5a848002e349de06d4bc820a"), "forwardSortationArea" : "X0A" }
{ "_id" : ObjectId("5a848002e349de06d4bc820b"), "forwardSortationArea" : "C1A" }

# disconnect from mongodb
quit()
```

### Run `GraphQL API`

Move to `nrcan_api\api` folder.

`API` utilizes Apollo Engine to monitor activities on host with `GraphQL` website.
Apollo Engine is a monitoring/logging layer that gives us out-of-the-box diagnostic information about our graphql instance. You'll need your own API key to get the API running, so [sign up for one here](https://engine.apollographql.com/login).
Key looks similar to: `service:yname-8241:lQ3g_8Yojs4stdIWqwwj-bQ`

Set following variables:
```sh
set NRCAN_DB_CONNECTION_STRING=mongodb://localhost:27017
set NRCAN_DB_NAME=energuide
set NRCAN_COLLECTION_NAME=dwellings
set NRCAN_ENGINE_API_KEY=service:yname-8241:lQ3g_8Yojs4stdIWqwwj-bQ
```

Make sure `yarn` is installed

```sh
# should return a version number
yarn --version
```
If `yarn` is not installed, run `npm install --global yarn` to install.

Next command start `GraphQL`
```sh
yarn start
```

### Using the API locally

The API should be running now! Yes!! 🎉🎉🎉

Check it out at [http://localhost:3000/graphiql](http://localhost:3000/graphiql)

Try out this query to get you going.

```
{
  dwellingsInFSA(
    forwardSortationArea: "C1A"
  ) {
    results {
      yearBuilt
      city
    }
  }
}
```

<sup>Or just [click here](http://localhost:3000/graphiql?query=%7B%0A%20%20dwellingsInFSA(%0A%20%20%20%20forwardSortationArea%3A%20%22C1A%22%0A%20%20)%20%7B%0A%20%20%20%20results%20%7B%0A%20%20%20%20%20%20yearBuilt%0A%20%20%20%20%20%20city%0A%20%20%20%20%7D%0A%20%20%7D%0A%7D)</sup>
