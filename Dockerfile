FROM ubuntu:20.04

WORKDIR /app
COPY . /app

RUN apt-get update && apt-get install -y \
    curl

RUN curl -Ls https://github.com/testappio/cli/releases/latest/download/install | bash

RUN chmod +x /app/entrypoint.sh

ENTRYPOINT [ "/app/entrypoint.sh" ]

