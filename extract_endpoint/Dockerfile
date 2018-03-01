FROM python:3
MAINTAINER Steven Zinck <steven.zinck@cds-snc.ca>
LABEL Description="Python ETL Endpoint" Vendor="Canadian Digital Service"


ADD . . 
RUN pip install -r requirements.txt 
RUN pip install -e .

CMD ["python", "src/extract_endpoint/endpoint.py"]
