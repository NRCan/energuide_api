FROM node:9.0-alpine
MAINTAINER Mike Williamson <mike.williamson@tbs-sct.gc.ca>
LABEL Description="Node API" Vendor="Canadian Digital Service"

WORKDIR /app
USER node
ADD . .

EXPOSE 3000
CMD yarn start
