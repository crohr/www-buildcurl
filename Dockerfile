FROM ubuntu:16.04
RUN apt-get update -qq && apt-get install -y apache2 markdown ruby openssh-client && apt-get clean
RUN gem install dotenv -v 2.2.1 --no-ri --no-rdoc
RUN a2dissite 000-default && a2enmod cgi
COPY . /opt/buildcurl
RUN cp /opt/buildcurl/conf/buildcurl.conf /etc/apache2/sites-enabled/buildcurl.conf
EXPOSE 80
CMD ["/opt/buildcurl/entrypoint.sh"]
