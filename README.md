# NRCAN's Energuide API

CircleCI Status: [![CircleCI](https://circleci.com/gh/cds-snc/nrcan_api.svg?style=svg)](https://circleci.com/gh/cds-snc/nrcan_api)

This is the API for NRCAN's Energuide data.

This project is composed of two parts: the API itself and the ETL process that produces the data the API will serve.
There are further details in the readme for each of the respective portions of the project.

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

### Using the API locally

The API should be running now! Yes!! 🎉🎉🎉

Check it out at [http://localhost:3000/graphiql]()

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
