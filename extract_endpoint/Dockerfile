FROM python:3.6
MAINTAINER Steven Zinck <steven.zinck@cds-snc.ca>
LABEL Description="Python ETL Endpoint" Vendor="Canadian Digital Service"

# Set version in .circlei/config.yml for docker build

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
RUN pip install -e .
CMD ["gunicorn", "--pythonpath=src/extract_endpoint", "--bind=0.0.0.0:5000", "endpoint:App"]
