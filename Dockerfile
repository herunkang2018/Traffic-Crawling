# This dockerfile allows to run an crawl inside a docker container

# Pull base image.
FROM debian:stable-slim

# Install required packages.
RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get --assume-yes --yes install sudo build-essential autoconf git zip unzip xz-utils
RUN DEBIAN_FRONTEND=noninteractive apt-get --assume-yes --yes install libtool libevent-dev libssl-dev
RUN echo "http://ftp.de.debian.org/debian testing main" >> /etc/apt/sources.list
RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get -t testing --assume-yes --yes install python3 python3-dev python3-setuptools python3-pip
RUN DEBIAN_FRONTEND=noninteractive apt-get --assume-yes --yes install net-tools ethtool tshark libpcap-dev
RUN DEBIAN_FRONTEND=noninteractive apt-get --assume-yes --yes install xvfb firefox-esr
RUN apt-get clean \
	&& rm -rf /var/lib/apt/lists/*

# Install python3 requirements.
RUN pip3 install --upgrade pip
RUN pip3 install requests

# add host user to container
RUN adduser --system --group --disabled-password --gecos '' --shell /bin/bash docker

# download geckodriver
ADD https://github.com/mozilla/geckodriver/releases/download/v0.19.0/geckodriver-v0.19.0-linux64.tar.gz /bin/
RUN tar -zxvf /bin/geckodriver* -C /bin/
ENV PATH /bin/geckodriver:$PATH

# download firefox-55
ADD https://ftp.mozilla.org/pub/firefox/releases/55.0.1/linux-x86_64/en-US/firefox-55.0.1.tar.bz2 /bin/
RUN tar -xf /bin/firefox-55* -C /bin/
ENV PATH /bin/firefox/firefox:$PATH