#!/usr/bin/env ruby

require 'cgi'

cgi = CGI.new
cgi.print cgi.header({"type" => "text/plain", "status" => "200"})
cgi.print "OK\n"
