FROM alpine:latest

# install python3 (don't cache it)
RUN apk add --no-cache python3 py3-pip

# create and checkout working directory
WORKDIR /app

# Copy over source code
COPY . /app

# install requirements
RUN pip --no-cache-dir install -r requirements.txt

RUN chmod +x start.sh
# RUN chmod +x create_docs.sh

EXPOSE 5000

ENTRYPOINT ["./flask_run.sh"]
# CMD ["./create_docs.sh"]