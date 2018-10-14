FROM python:3.7

ENV PYTHONUNBUFFERED 1
RUN apt-get update && apt-get upgrade -y && apt-get install git -y
RUN pip install --upgrade pip

RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app
ADD requirements.txt /usr/src/app
RUN pip install -r requirements.txt

ADD . /usr/src/app
COPY fixtures/ /docker-entrypoint-initdb.d/
RUN ["chmod", "+x","/usr/src/app/docker-entrypoint.sh"]
RUN ["chmod", "+x","/usr/src/app/run.sh"]

EXPOSE 8000

ENTRYPOINT ["/usr/src/app/docker-entrypoint.sh"]
