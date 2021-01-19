## BASE IMAGE ##
FROM alpine:latest as baseimage

# install python3 (don't cache it)
RUN apk add --no-cache python3 py3-pip
RUN apk add --update make

# create and checkout working directory
WORKDIR /app

# copy files
COPY bpm/ /app/bpm
COPY ./.flaskenv /app
COPY docs/ /app/docs
COPY requirements.txt /app
COPY README.rst /app

# install requirements
RUN pip --no-cache-dir install -r requirements.txt

RUN cd docs; make clean html; cd ..;


## BACKEND ##
FROM baseimage as backend

EXPOSE 5000

ENTRYPOINT ["gunicorn", "--bind=0.0.0.0:5000", "bpm:create_app()"]


## DOCS ##
FROM nginx as documentation

COPY --from=baseimage app/docs/build/html /usr/share/nginx/html

EXPOSE 80

ENTRYPOINT ["nginx", "-g", "daemon off;"]