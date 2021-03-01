FROM python:3.7-alpine

WORKDIR /watchlist

RUN apk update && apk upgrade && apk add --update alpine-sdk
COPY . .
RUN make install

CMD make run-huey & make run-django
