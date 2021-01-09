FROM python:3.9

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN mkdir /social-network
WORKDIR /social-network

ADD requirements.txt /social-network/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /social-network/
RUN chmod +x ./compose/django/entrypoint.sh