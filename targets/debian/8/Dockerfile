FROM debian:8

RUN apt-get update -qq && apt-get install -y \
	git \
	lsb-release \
	curl \
	pkg-config \
	libssl1.0.0 \
	libmysqlclient-dev \
	libpq-dev \
	libsqlite3-0 \
	libevent-dev \
	libssl-dev \
	libcurl4-openssl-dev \
	libxml2-dev \
	libxslt1-dev \
	libreadline-dev \
	subversion \
	zip \
	bzip2 \
	coreutils \
	tar \
	libtool \
	build-essential \
	autoconf \
	libbz2-dev \
	libpng-dev \
	libjpeg-dev \
	libfreetype6-dev \
	&& apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN echo "debian:8" > /etc/version
