# Energuide

This is the API for NRCAN's Energuide data.

## Running the server

Running the sever requires a SQL server running somewhere and the following environmental variables defined:

* NRCAN_API_USERNAME
* NRCAN_API_PASSWORD
* NRCAN_API_HOST
* NRCAN_API_DATABASE
* NRCAN_ENGINE_API_KEY

With those defined you can run the server like this:

```sh
> yarn && yarn run build
> NRCAN_DB_CONNECTION_STRING="mongodb://localhost:27017" \
	NRCAN_DB_NAME="energuide" \
	NRCAN_COLLECTION_NAME="buildings" \
	NRCAN_ENGINE_API_KEY="your_apollo_engine_api_key" yarn start
```

The API server is available as a Docker container and can be run with:
```
docker run -it -e "NRCAN_ENGINE_API_KEY=your_apollo_engine_api_key" -e "NRCAN_DB_CONNECTION_STRING=mongodb://localhost:27017" -e "NRCAN_DB_NAME=energuide" -e "NRCAN_COLLECTION_NAME=buildings" --net="host" -p 3000:3000 cdssnc/nrcan_api

```

The container will need network connectivity to the database (obviously) so
ensure that docker networking is setup up in such a way to allow that. The
above command uses the `--net="host"` option to connect the container to the
SQLServer database installed on the host machine. Adjust as needed.
Monitoring and caching is done with [Apollo Engine](https://engine.apollographql.com), hence the API key.

Assuming the DB credentials/connectivity is correct, the command above will
start a graphql endpoint that will respond to the following `curl` commands:

```
curl -s -H "Content-Type: application/json" -d '{"query": "{ evaluations(withinPolygon: [ {lng: -150.82031249999997, lat: -0.3515602939922709} {lng: -41.8359375, lat: -0.3515602939922709}, {lng: -41.8359375, lat: 73.62778879339942}, {lng: -150.82031249999997, lat: 73.62778879339942}, {lng: -150.82031249999997, lat: -0.3515602939922709}, ]) { yearBuilt floorArea } }"}'  "localhost:3000/graphql"


# or

curl -s -H "Content-Type: application/json" -d '{"query": "{ evaluationsFor(account: 1234) { yearBuilt floorArea } }"}'  "localhost:3000/graphql"
```


## Running the tests

```sh
> yarn test
```
