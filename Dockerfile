FROM ubuntu:rolling

MAINTAINER cgrant@ou.edu

RUN apt-get update && apt-get install -y locales && rm -rf /var/lib/apt/lists/* \
    && localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8
ENV LANG en_US.utf8

# Python tools
RUN apt-get update && apt-get upgrade -y && apt-get install -y python3-pip ipython3

# Shell debug tools
RUN apt-get install -y vim nmap iputils-ping ssh netcat htop slurm net-tools

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# Copy all keys and other files
COPY . /usr/src/app

# Other utilities files
RUN bash utils/get_gecko.sh && bash utils/get_phantomjs.sh

# Unbuffer to see logs with docker logs <containername>
ENV PYTHONUNBUFFERED=1

RUN pip3 install pipenv

#CMD ["pipenv", "shell"]
