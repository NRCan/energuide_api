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

## Running the tests

```sh
> yarn test
```
