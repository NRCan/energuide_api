# NRCAN's Energuide API

CircleCI Status: [![CircleCI](https://circleci.com/gh/cds-snc/nrcan_api.svg?style=svg)](https://circleci.com/gh/cds-snc/nrcan_api)

This is the API for NRCAN's Energuide data.

This project is composed of two parts: the API itself and the ETL process that produces the data the API will serve.
There are further details in the readme for each of the respective portions of the project.

- [Windows Installation Instructions](#windows-installation)
- [MacOS Installation Instructions](#tldr)

## Quickstart

### TL;DR

If you're really keen (and on a Mac), this should do you. Continue reading for more details.

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

The Python code in `/python` transforms the data from its default formatting by NRCAN and then inserts it into our Mongo database. More details can be found in the [README](https://github.com/cds-snc/nrcan_api/blob/master/python/README.md).

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
make run
```

This will
- install the needed JavaScript dependencies
- build the app
- serve it up locally

## Windows installation

### Install required software

1. Download and install python from [here](https://www.python.org/downloads/release/python-364/).
Version 3.6.4 or higher is required.

2. Download current version of mongoDB community server from [here](https://www.mongodb.com/download-center#community).

3. Download Node.js from [here](https://nodejs.org/en/download/). Version >=8.x of Node is required.

Check if the libraries are accessible by running the following commands in a terminal window
```
python --version

mongo --version

node --version
```
If version is not shown, the path to the library has to be added to the 'PATH' environment variable in system properties

### Run python extractor

Installing Python applications in a `virtualenv` is considered best practice. To do so, run:
```
cd \python
python -m venv env
env\Scripts\activate.bat
```
Inside an activated `virtualenv`, and from the python folder of the project, run:

```
pip install -r requirements.txt
pip install -e .
```
"." is the part of command

`Mongodb` must be started before going to the next step. Open new terminal window and type
```
md \data\db    #required run just first time
mongo
```
Keep this window open to continue running the database and open a new one to finish extracting the data.

Finish python part of installation.

Following command drop existing `energuide mongodb` test data.
```
mongo energuide --eval "db.dwellings.drop()"
```

Run python command:
```
energuide extract --infile tests/randomized_energuide_data.csv --outfile allthedata.zip  #extract from csv to zip file
energuide load --filename allthedata.zip	#load data into mongodb
del allthedata.zip							#delete zip file
```
Unit tests for the python code.
```
pytest tests
mypy src tests --ignore-missing-imports
```
Open new terminal window. Run following command to connect to `energuide`db:
```
mongo												#open db client
show dbs											#show db exists
use energuide										#connect energuide schema
db.dwellings.count()								#total number of entry data. Should be 7
db.dwellings.find({}, {'forwardSortationArea': 1})	#select some fields
#result shuld looks like:
{ "_id" : ObjectId("5a848002e349de06d4bc8205"), "forwardSortationArea" : "T0J" }
{ "_id" : ObjectId("5a848002e349de06d4bc8206"), "forwardSortationArea" : "A2H" }
{ "_id" : ObjectId("5a848002e349de06d4bc8207"), "forwardSortationArea" : "Y1A" }
{ "_id" : ObjectId("5a848002e349de06d4bc8208"), "forwardSortationArea" : "G1A" }
{ "_id" : ObjectId("5a848002e349de06d4bc8209"), "forwardSortationArea" : "B2R" }
{ "_id" : ObjectId("5a848002e349de06d4bc820a"), "forwardSortationArea" : "X0A" }
{ "_id" : ObjectId("5a848002e349de06d4bc820b"), "forwardSortationArea" : "C1A" }
quit()												#disconnect for db
```

### Run `GraphQL API`  

Move to `nrcan_api\api` folder
`API` utilizes Apollo Engine to monitor activities on host with `GraphQL` website.
Apollo Engine is a monitoring/logging layer that gives us out-of-the-box diagnostic information about our graphql instance. You'll need your own API key to get the API running, so [sign up for one here](https://engine.apollographql.com/login).
Key looks similar to: `service:yname-8241:lQ3g_8Yojs4stdIWqwwj-bQ`

Set following variables:
```
set NRCAN_DB_CONNECTION_STRING=mongodb://localhost:27017
set NRCAN_DB_NAME=energuide
set NRCAN_COLLECTION_NAME=dwellings
set NRCAN_ENGINE_API_KEY=service:yname-8241:lQ3g_8Yojs4stdIWqwwj-bQ
```

Next command start `GraphQL`
```
npm run start
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

<super>Or just [click here](http://localhost:3000/graphiql?query=%7B%0A%20%20dwellingsInFSA(%0A%20%20%20%20forwardSortationArea%3A%20%22C1A%22%0A%20%20)%20%7B%0A%20%20%20%20results%20%7B%0A%20%20%20%20yearBuilt%0A%20%20%20%20city%0A%20%20%20%20%7D%0A%20%20%7D%0A%7D)</super>
