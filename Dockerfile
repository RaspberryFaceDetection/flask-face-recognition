FROM python:3.6.1
MAINTAINER Vladyslav Kromkach

WORKDIR /app

RUN apt-get update -y && \
    apt-get install build-essential cmake pkg-config -y

RUN pip install dlib==19.9.0

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY . /app

ENTRYPOINT [ "python3" ]

CMD [ "app.py" ]
