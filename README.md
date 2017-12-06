# Energuide

This is the API for NRCAN's Energuide data.

## Running the server

Running the sever requires a SQL server running somewhere and the following environmental variables defined:

* NRCAN_API_USERNAME
* NRCAN_API_PASSWORD
* NRCAN_API_HOST
* NRCAN_API_DATABASE

With those defined you can run the server like this:

```sh
> yarn run build
> yarn start
```

The API server is available as a Docker container and can be run with:
```
docker run -it -e "NRCAN_API_USERNAME=dbusername" -e "NRCAN_API_PASSWORD=dbpassword" -e "NRCAN_API_HOST=dburl" -e "NRCAN_API_DATABASE=dbname" --net="host" -p 3000:3000 cdssnc/nrcan_api
```

The container will need network connectivity to the database (obviously) so
ensure that docker networking is setup up in such a way to allow that. The
above command uses the `--net="host"` option to connect the container to the
SQLServer database installed on the host machine. Adjust as needed.

Assuming the DB credentials/connectivity is correct, the command above will
start a graphql endpoint that will respond to the following `curl`:

```
curl -v -H "Content-Type: application/json" -d '{"query": "{ evaluations { yearBuilt } }"}'  "localhost:3000/graphql"
```

## Running the tests

```sh
> yarn test
```
