FROM python:3-alpine3.15

RUN mkdir /app

COPY dirty_channels.txt /app/dirty_channels.txt
COPY requirements.txt /app/requirements.txt
COPY messages.txt /app/messages.txt
COPY main.py /app/main.py

WORKDIR /app

RUN apk update --no-cache && apk upgrade \
    && python -m pip install --upgrade pip \
    && pip install -r requirements.txt

ENTRYPOINT ["python", "main.py"]