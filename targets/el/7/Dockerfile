from centos:7

run yum makecache fast

run yum -y install \
  git \
  vim \
  sudo \
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
  ruby \
  autoconf subversion zip file patch \
  && yum clean all

RUN echo "el:7" > /etc/version
