FROM debian:8

RUN apt-get update -qq

RUN apt-get install -y git \
	sudo \
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

RUN curl https://s3.amazonaws.com/pkgr-buildpack-ruby/current/debian-8/ruby-2.2.2.tgz -o - | tar xzf - -C /usr/local

RUN echo "debian:8" > /etc/version
