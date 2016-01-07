FROM debian:8

RUN apt-get update -qq && apt-get install -y \
	git \
	lsb-release \
	curl \
	libssl1.0.0 \
	libmysqlclient-dev \
	libpq-dev \
	libsqlite3-0 \
	libevent-dev \
	libssl-dev \
	libxml2-dev \
	libxslt1-dev \
	libreadline-dev \
	subversion \
	zip \
	coreutils \
	tar \
	build-essential \
	autoconf \
	&& apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN echo "debian:8" > /etc/version
