FROM ubuntu:14.04

RUN locale-gen en_US.UTF-8 && update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
RUN apt-get update -qq && apt-get -y install markdown ruby apache2 curl git htop && apt-get clean
RUN curl https://get.docker.com/builds/Linux/x86_64/docker-1.9.1.tgz -o - | tar xzf - -C /
RUN gem install aws-sdk dotenv --no-ri --no-rdoc
RUN groupadd docker && usermod -aG docker www-data && a2enmod cgi
RUN rm -f /etc/apache2/sites-enabled/*.conf
ADD conf/buildcurl.conf /etc/apache2/sites-enabled/buildcurl.conf
ADD . /opt/buildcurl
ADD ./entrypoint.sh /entrypoint.sh
RUN mkdir -p /opt/buildcurl/cache && chmod 2777 /opt/buildcurl/cache
WORKDIR /opt/buildcurl
ENTRYPOINT ["/entrypoint.sh"]
CMD ["-DFOREGROUND"]
EXPOSE 80
