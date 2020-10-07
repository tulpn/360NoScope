FROM python:3.8.2

WORKDIR /usr/src/app

COPY ./noscope/requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY ./noscope/ .

