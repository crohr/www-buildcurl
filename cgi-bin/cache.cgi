#!/usr/bin/env ruby
require 'cgi'
require 'fileutils'
require 'dotenv'

SOURCE = ENV.fetch('SOURCE') { File.dirname(Dir.pwd) }
Dotenv.load File.join(SOURCE, ".env")
cgi = CGI.new

case ENV['PATH_INFO']
when /^\/([^\/]+)$/
  filename = $1
  STDERR.puts filename.inspect
  cache_file = "/tmp/#{filename}"
  if File.exists?(cache_file)
    cgi.print cgi.header({"status" => 200, "type" => "application/octet-stream"})
    IO.copy_stream(File.open(cache_file, "rb"), STDOUT)
    FileUtils.rm_f(cache_file)
  else
    cgi.print cgi.header({"type" => "text/plain", "status" => 410})
    cgi.print "410 Gone - Unknown file\n\n"
    cgi.print "Note:\n"
    cgi.print "  Tarball files are removed after the first download.\n"
    cgi.print "  Please retry the compilation at #{cgi.host}.\n"
  end
else
  cgi.print cgi.header({"type" => "text/plain", "status" => 400})
  cgi.print "Unsupported command\n"
end
