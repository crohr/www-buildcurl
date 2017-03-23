FROM oraclelinux:7

RUN yum makecache fast && yum -y install \
	git \
	wget \
	curl \
	tar \
	openssl-devel \
	readline-devel \
	libxml2-devel \
	libxslt-devel \
	libevent-devel \
	postgresql-devel \
	mysql-devel \
	sqlite-devel \
	gcc \
	gcc-c++ \
	kernel-devel \
	cmake make \
	autoconf \
	subversion \
	zip \
	file \
	patch \
	bzip2-devel \
	bzip2 \
	libicu-devel \
	libtool \
	libpng-devel \
	libjpeg-devel \
	freetype-devel \
	automake \
	libtool \
	curl-devel \
	&& yum clean all

RUN echo "ol:7" > /etc/version
