FROM python:3.9.0

FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

WORKDIR /app
 
ADD . /app

COPY ./requirements.txt /app/requirements.txt


RUN pip install --upgrade pip

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./app /app
