#!/usr/bin/env ruby
require 'cgi'
require 'fileutils'

SOURCE = ENV.fetch('SOURCE') { File.dirname(Dir.pwd) }
CACHE_DIR = ENV.fetch('CACHE_DIR') { File.join(SOURCE, "cache") }
FileUtils.mkdir_p CACHE_DIR

cgi = CGI.new

case ENV['PATH_INFO']
when /^\/([^\/]+)$/
  filename = $1
  cache_file = File.join(CACHE_DIR, filename)
  if File.exists?(cache_file)
    if File.extname(filename) == ".log"
      cgi.print cgi.header({"type" => "text/plain", "status" => 200})
    else
      cgi.print cgi.header({"type" => "application/x-compressed", "status" => 200})
    end
    File.open(cache_file, "r").each_line do |line|
      cgi.print line
    end
  else
    cgi.print cgi.header({"type" => "text/plain", "status" => 404})
    cgi.print "Unknown cache file\n"
  end
else
  cgi.print cgi.header({"type" => "text/plain", "status" => 400})
  cgi.print "Unsupported command\n"
end
