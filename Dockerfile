# for flask: docker run --env-file=.flaskenv image ahelp-api run
FROM python:3.10.7-slim-buster

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app

COPY requirements.txt ./

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY ahelp ahelp/
COPY migrations migrations/

EXPOSE 5000
