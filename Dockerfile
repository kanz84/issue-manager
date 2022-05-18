# syntax=docker/dockerfile:1
FROM python:3.6-alpine

RUN apk update && apk upgrade && pip install -U pip
RUN apk add --update --no-cache --virtual .tmp-build-deps alpine-sdk make gcc python3-dev libxslt-dev \
        libxml2-dev libc-dev openssl-dev libffi-dev zlib-dev py-pip openssh libpq-dev postgresql-client \
        linux-headers postgresql-dev

#RUN addgroup admin
#RUN adduser --disabled-password --ingroup "admin" --gecos "Admin" --home "/home/admin" admin
#
#
#USER admin
#WORKDIR /home/admin

RUN ping 8.8.8.8 -c 1
RUN ping google.com -c 1

RUN mkdir workspace
RUN mkdir /workspace/project
RUN mkdir /workspace/files
RUN mkdir /workspace/files/static
RUN mkdir /workspace/files/media
RUN mkdir /workspace/files/log

WORKDIR /workspace/project

COPY requirements.txt .
RUN pip install -r requirements.txt

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
COPY . .

