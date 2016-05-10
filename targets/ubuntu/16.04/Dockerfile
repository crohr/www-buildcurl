FROM ubuntu:16.04

RUN apt-get -qq update && apt-get install -y \
	git \
	wget \
	lsb-release \
	python \
	curl \
	libssl1.0.0 \
	libmysqlclient-dev \
	libpq-dev \
	pkg-config \
	libsqlite3-0 \
	libevent-dev \
	libssl-dev \
	libxml2-dev \
	libcurl4-openssl-dev \
	libxslt1-dev \
	libicu-dev \
	libreadline-dev \
	build-essential \
	subversion \
	zip \
	coreutils \
	tar \
	autoconf \
	libbz2-dev \
	bzip2 \
	libtool \
	libpng-dev \
	libjpeg-dev \
	libfreetype6-dev \
	&& apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN echo "ubuntu:16.04" > /etc/version
