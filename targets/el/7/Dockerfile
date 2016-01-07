FROM centos:7

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
  ruby \
  autoconf subversion zip file patch \
  && yum clean all

RUN echo "el:7" > /etc/version
