from debian:7

RUN apt-get update -qq && apt-get -y install \
	git \
	wget \
	pkg-config \
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
	build-essential \
	libcurl4-openssl-dev \
	subversion \
	zip \
	bzip2 \
	libtool \
	coreutils \
	tar \
	autoconf \
	libbz2-dev \
	libpng-dev \
	libjpeg-dev \
	libfreetype6-dev \
	apt-transport-https \
	&& apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN echo "debian:7" > /etc/version
