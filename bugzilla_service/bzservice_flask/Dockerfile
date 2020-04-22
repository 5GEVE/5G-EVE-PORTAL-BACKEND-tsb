FROM python:3.7.1

LABEL Author="Gines Garcia Aviles"
LABEL E-mail="gigarcia@it.uc3m.es"
LABEL version="0.1b"

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

WORKDIR /

COPY ./requirements.txt /requirements.txt
RUN pip3 install -r requirements.txt

RUN mkdir bzservice_flask

ADD ./app /bzservice_flask/app
ADD ./bugzilla_app.py /bzservice_flask
#ADD ./keycloak.json /bzservice_flask/app/keycloak

WORKDIR /bzservice_flask

CMD [ "python3", "bugzilla_app.py" ]
