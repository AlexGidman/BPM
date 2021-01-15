FROM alpine:latest

# install python3 (don't cache it)
RUN apk add --no-cache python3 py3-pip

# create and checkout working directory
WORKDIR /app

# copy api key env variables - might need to be done in compose

# copy over bpm source code
COPY bpm/ /app/bpm
COPY ./.flaskenv /app
COPY ./requirements.txt /app

# copy over docs
COPY docs/ /app/docs
COPY ./create_docs.sh /app

# # install requirements
RUN pip --no-cache-dir install -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["flask", "run"]

# RUN chmod +x create_docs.sh
# ["./create_docs.sh"]