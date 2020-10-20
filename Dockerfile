FROM python:3.7
ENV PYTHONUNBUFFERED 1

##########################################################################
## Install the container
## Copy files one by one and split commands to use docker cache
##########################################################################

RUN mkdir /code
WORKDIR /code

COPY Pipfile Pipfile.lock /code/

#########################################################################
## Install packages
#########################################################################

RUN apt-get update
RUN apt-get install -y postgresql
RUN pip install pipenv
RUN pipenv install --system --dev

#########################################################################
## Copy everything into the container
#########################################################################

COPY . /code

#########################################################################
## Set the entrypoint
#########################################################################
EXPOSE 8000
ENTRYPOINT ["/code/entrypoint.sh"]
