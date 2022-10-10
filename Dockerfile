# pull the official base image
FROM python:3


# set work directory
WORKDIR /usr/src/app

#RUN apk add -u gcc musl-dev

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get install -y --no-install-recommends postgresql-client \
    netcat


# install dependencies
RUN pip install --upgrade pip 
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# copy project
COPY . .
RUN chmod +x ./entrypoint.prod.sh


ENTRYPOINT ["/usr/src/app/entrypoint.prod.sh"]

