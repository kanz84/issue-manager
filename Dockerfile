# syntax=docker/dockerfile:1
FROM python:3.6-alpine
RUN apk update && apk upgrade && pip install -U pip
RUN apk add --update alpine-sdk make gcc python3-dev libxslt-dev libxml2-dev libc-dev openssl-dev libffi-dev zlib-dev py-pip openssh
# RUN apk add gcc musl-dev linux-headers python3-dev

WORKDIR /code
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
EXPOSE 8000
COPY . .
RUN pip install -r requirements.txt

