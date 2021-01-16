FROM alpine:latest as baseimage

# install python3 (don't cache it)
RUN apk add --no-cache python3 py3-pip

# create and checkout working directory
WORKDIR /app

# copy over bpm source code
COPY bpm/ /app/bpm
COPY ./.flaskenv /app

# install requirements
RUN pip --no-cache-dir install -r bpm/requirements.txt


## BACKEND ##
FROM baseimage as backend

EXPOSE 5000

ENTRYPOINT ["flask", "run"]
