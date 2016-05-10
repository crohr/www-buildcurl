FROM fedora:20

# required because otherwise openssl-libs are broken
# https://fedorahosted.org/spin-kickstarts/ticket/55
RUN sed -i "s|enabled=0|enabled=1|g" /etc/yum.repos.d/fedora-updates-testing.repo

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
	gcc gcc-c++ kernel-devel \
	cmake make \
	autoconf \
	subversion \
	zip \
	file \
	patch \
	libtool \
	curl-devel \
	bzip2-devel \
	bzip2 \
	libicu-devel \
	libpng-devel \
	libjpeg-devel \
	freetype-devel \
	&& yum clean all

RUN echo "fedora:20" > /etc/version
