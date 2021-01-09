FROM python:3.9
RUN mkdir /bot
WORKDIR /bot

ADD requirements.txt /bot/
RUN pip install --no-cache-dir -r requirements.txt

COPY sources /bot
