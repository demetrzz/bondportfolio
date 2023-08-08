# syntax=docker/dockerfile:1
FROM python:3.11.4-alpine3.18
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /bondportfolio_project
COPY requirements.txt /bondportfolio_project/
RUN pip install -r requirements.txt
COPY . /bondportfolio_project/