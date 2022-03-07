# syntax=docker/dockerfile:1
FROM python:3.6-alpine
RUN apk update && apk upgrade && pip install -U pip
RUN apk add --update alpine-sdk make gcc python3-dev libxslt-dev libxml2-dev libc-dev openssl-dev libffi-dev zlib-dev py-pip openssh libpq-dev postgresql-client
# RUN apk add gcc musl-dev linux-headers python3-dev

RUN apk add --update --no-cache --virtual .tmp-build-deps linux-headers postgresql-dev

COPY requirements.txt ./code/
WORKDIR /code
RUN pip install -r requirements.txt


ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
COPY . .

