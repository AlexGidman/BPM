FROM alpine:latest as baseimage

# install python3 (don't cache it)
RUN apk add --no-cache python3 py3-pip
RUN apk add --update make

# create and checkout working directory
WORKDIR /app

# copy over bpm source code
COPY bpm/ /app/bpm
COPY ./.flaskenv /app

# copy docs files
COPY docs/ /app/docs
COPY requirements.txt /app
COPY README.rst /app

# # install requirements
RUN pip --no-cache-dir install -r requirements.txt

## BACKEND ##
FROM baseimage as backend

EXPOSE 5000

ENTRYPOINT ["flask", "run"]


## DOCS BUILD ##
FROM baseimage as documentation_builder

RUN cd docs; make clean html; cd ..;

# ## DOCS SERVED ON NGINX
FROM nginx as documentation

COPY --from=documentation_builder app/docs/build/html /usr/share/nginx/html

EXPOSE 80

ENTRYPOINT ["nginx", "-g", "daemon off;"]