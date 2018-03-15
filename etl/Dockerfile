FROM python:3.6
MAINTAINER Steven Zinck <steven.zinck@cds-snc.ca>
LABEL Description="NRCan ETL" Vendor="Canadian Digital Service"

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
RUN pip install -e .
CMD ["gunicorn", "--pythonpath=src/energuide", "--bind=0.0.0.0:5010", "flask_app:App"]
