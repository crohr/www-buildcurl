from debian:7

RUN apt-get update -qq

RUN apt-get -y install git vim \
  sudo \
  wget \
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
  subversion zip coreutils tar autoconf \
  && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN cd /usr/local/src/ && wget -q http://pyyaml.org/download/libyaml/yaml-0.1.6.tar.gz && tar xzf yaml-0.1.6.tar.gz && cd /usr/local/src/yaml-0.1.6/ && ./configure --prefix=/usr/local && make && make install && rm -rf /usr/local/src/*

RUN cd /usr/local/src/ && wget -q ftp://ftp.ruby-lang.org/pub/ruby/1.9/ruby-1.9.3-p429.tar.gz && tar xzf ruby-1.9.3-p429.tar.gz && cd /usr/local/src/ruby-1.9.3-p429/ && ./configure --prefix=/usr/local --enable-shared --disable-install-doc --with-opt-dir=/usr/local/lib --with-openssl-dir=/usr/local && make && make install && rm -rf /usr/local/src/*

RUN cd /usr/local/src/ && wget -q http://production.cf.rubygems.org/rubygems/rubygems-2.2.1.tgz && tar xzf rubygems-2.2.1.tgz && cd /usr/local/src/rubygems-2.2.1/ && ruby setup.rb --prefix=/usr/local && rm -rf /usr/local/src/*

RUN echo "debian:7" > /etc/version
