FROM python:3.7

ENV PYTHONUNBUFFERED 1
RUN apt-get update && apt-get upgrade -y && apt-get install git -y

RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app
ADD requirements.txt /usr/src/app
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY fixtures/ /docker-entrypoint-initdb.d/

ADD happy_child happy_child
ADD infrastructure infrastructure
ADD services services
ADD static static
ADD templates templates
ADD views views
ADD *.py ./
ADD *.sh ./

RUN ["chmod", "+x","/usr/src/app/docker-entrypoint.sh"]
RUN ["chmod", "+x","/usr/src/app/run_develop.sh"]
RUN ["chmod", "+x","/usr/src/app/run.sh"]

EXPOSE 8000

ENTRYPOINT ["/usr/src/app/docker-entrypoint.sh"]
