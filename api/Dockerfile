FROM node:9-alpine
MAINTAINER Mike Williamson <mike.williamson@tbs-sct.gc.ca>
LABEL Description="Node API" Vendor="Canadian Digital Service"

WORKDIR /app
ADD . .
RUN yarn install && yarn build

USER node

EXPOSE 3000
CMD yarn start
