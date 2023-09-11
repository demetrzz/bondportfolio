# syntax=docker/dockerfile:1
FROM python:3.11.5-bookworm
#RUN apk add --no-cache --update \
#    python3 python3-dev gcc \
#    gfortran musl-dev \
#    libffi-dev openssl-dev
RUN pip3 install --upgrade pip setuptools
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /bondportfolio
COPY requirements.txt /bondportfolio
RUN pip install -r requirements.txt
COPY .. /bondportfolio/