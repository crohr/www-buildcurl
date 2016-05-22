FROM ubuntu:14.04

RUN apt-get update -qq && apt-get -y install ruby apache2 curl git htop && apt-get clean
RUN curl https://get.docker.com/builds/Linux/x86_64/docker-1.9.1.tgz -o - | tar xzf - -C /
RUN groupadd docker && usermod -aG docker www-data && a2enmod cgi
RUN rm -f /etc/apache2/sites-enabled/*.conf
ADD conf/buildcurl.conf /etc/apache2/sites-enabled/buildcurl.conf
ADD . /opt/buildcurl
RUN mkdir -p /opt/buildcurl/cache && chmod 2777 /opt/buildcurl/cache
RUN echo "BUILDCURL_URL=http://localhost:80" > /opt/buildcurl/.env
WORKDIR /opt/buildcurl
ENTRYPOINT ["/usr/sbin/apache2ctl"]
CMD ["-DFOREGROUND"]
EXPOSE 80
