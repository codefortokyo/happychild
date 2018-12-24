FROM python:3.7

ENV JAVA_HOME /usr/lib/jvm/java-8-oracle
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get upgrade -y && apt-get install git -y

RUN echo oracle-java8-installer shared/accepted-oracle-license-v1-1 select true | debconf-set-selections && \
    apt-get update && \
    apt-get install -y software-properties-common && \
    add-apt-repository -y ppa:webupd8team/java && \
    apt-get update && \
    apt-get install -y  --allow-unauthenticated oracle-java8-installer

RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app
ADD requirements.txt /usr/src/app
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY fixtures/ /docker-entrypoint-initdb.d/

ADD happychild happychild
ADD infrastructure infrastructure
ADD services services
ADD static static
ADD templates templates
ADD views views
ADD resources resources
ADD *.py ./
ADD *.sh ./

RUN ["chmod", "+x","/usr/src/app/docker-entrypoint.sh"]
RUN ["chmod", "+x","/usr/src/app/run_develop.sh"]
RUN ["chmod", "+x","/usr/src/app/run.sh"]

EXPOSE 8000

ENTRYPOINT ["/usr/src/app/docker-entrypoint.sh"]
