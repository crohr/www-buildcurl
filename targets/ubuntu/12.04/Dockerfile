FROM ubuntu:12.04

RUN apt-get -qq update && apt-get -y install \
	git \
	wget \
	lsb-release \
	curl \
	pkg-config \
	libssl1.0.0 \
	libmysqlclient-dev \
	libpq-dev \
	libsqlite3-0 \
	libevent-dev \
	libssl-dev \
	libxml2-dev \
	libxslt1-dev \
	libreadline-dev \
	build-essential \
	libcurl4-openssl-dev \
	libicu-dev \
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

RUN echo "ubuntu:12.04" > /etc/version
