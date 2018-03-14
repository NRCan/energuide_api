## Run Locally

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
