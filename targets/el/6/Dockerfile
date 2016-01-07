FROM centos:6

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
  autoconf subversion zip file patch \
  ruby \
  && yum clean all

RUN echo "el:6" > /etc/version
