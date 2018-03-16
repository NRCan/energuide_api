FROM python:3.6
MAINTAINER Steven Zinck <steven.zinck@cds-snc.ca>
LABEL Description="NRCan ETL" Vendor="Canadian Digital Service"

# ------------------------
# SSH Server support
# ------------------------
RUN apt-get update \
    && apt-get install -y --no-install-recommends openssh-server \
    && echo "root:Docker!" | chpasswd
COPY sshd_config /etc/ssh/sshd_config
COPY init_container.sh /opt/startup/init_container.sh
RUN chmod 755 /opt/startup/init_container.sh

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
RUN pip install -e .

EXPOSE 2222 5010
ENTRYPOINT ["/opt/startup/init_container.sh"]
