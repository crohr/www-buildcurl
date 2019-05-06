from crohr/sles:11

RUN zypper ar --no-gpgcheck -t yast2 "http://storage.googleapis.com/pkgr-io-cache/SLES-11-SP4-DVD-x86_64-GM-DVD1" "SLES11 Server DVD1"
RUN zypper ar --no-gpgcheck -t yast2 "http://storage.googleapis.com/pkgr-io-cache/SLE-11-SP4-SDK-DVD-x86_64-GM-DVD1" "SLES11 SDK DVD1"

RUN zypper install -y \
	gcc \
	automake \
	gdbm-devel \
	libcurl-devel \
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
	pkg-config \
	curl \
	libevent-devel \
	libxml2-devel \
	libxslt-devel \
	openssl-certs \
	libtool \ 
	bzip2 \
	libbz2-devel \
	libjpeg-devel \
	libpng-devel \
	libicu-devel \
	freetype2-devel \
	postgresql94-devel \
	openssh \
	git \
	&& zypper clean --all

RUN ln -s /bin/true /usr/bin/logger
RUN echo "sles:11" > /etc/version
