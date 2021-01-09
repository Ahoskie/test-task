FROM python:3.9

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN mkdir /auth-service
WORKDIR /auth-service

ADD requirements.txt /auth-service/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /auth-service/
RUN chmod +x ./compose/django/entrypoint.sh
