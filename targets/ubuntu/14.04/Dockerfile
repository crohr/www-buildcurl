FROM ubuntu:14.04

RUN apt-get -qq update && apt-get install -y \
  git \
  wget \
  lsb-release \
  python \
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
  subversion zip coreutils tar autoconf \
  && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN echo "ubuntu:14.04" > /etc/version
