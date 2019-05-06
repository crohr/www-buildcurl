from crohr/sles:12

RUN zypper ar --no-gpgcheck -t yast2 "http://storage.googleapis.com/pkgr-io-cache/SLE-12-Server-DVD-x86_64-GM-DVD1" "SLES12 Server DVD1"
RUN zypper ar --no-gpgcheck -t yast2 "http://storage.googleapis.com/pkgr-io-cache/SLE-12-SDK-DVD-x86_64-GM-DVD1" "SLES12 SDK DVD1"

RUN zypper install -y \
	gcc \
	automake \
	gdbm-devel \
	libffi-devel \
	libopenssl-devel \
	ncurses-devel \
	readline-devel \
	zlib-devel \
	autoconf \
	zip \
	file \
	patch \
	zlib \
	gcc-c++ \
	wget \
	awk \
	make \
	curl \
	pkg-config \
	libevent-devel \
	libcurl-devel \
	libxml2-devel \
	libxslt-devel \
	ca-certificates \
	libtool \ 
	bzip2 \
	libbz2-devel \
	libjpeg-devel \
	libpng-devel \
	libicu-devel \
	freetype2-devel \
	postgresql-devel \
	openssh \
	git \
	rpmbuild \
	&& zypper clean

RUN ln -s /bin/true /usr/bin/logger
RUN echo "sles:12" > /etc/version
