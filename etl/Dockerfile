FROM python:3
LABEL Description="NRCan ETL" Vendor="Canadian Digital Service"

MAINTAINER Steven Zinck <steven.zinck@cds-snc.ca>

ADD . .

RUN pip install -r requirements.txt
RUN pip install -e .


