#!/usr/bin/env ruby
require 'cgi'
require 'fileutils'
require 'aws-sdk'
require 'dotenv'

SOURCE = ENV.fetch('SOURCE') { File.dirname(Dir.pwd) }
Dotenv.load File.join(SOURCE, ".env")
S3 = Aws::S3::Resource.new
BUCKET = S3.bucket(ENV.fetch('AWS_BUCKET'))
CACHE_URL = ENV.fetch('CACHE_URL') { ENV.fetch('BUILDCURL_URL') }

cgi = CGI.new

case ENV['PATH_INFO']
when /^\/([^\/]+)$/
  filename = $1
  cache_file = "cache/#{filename}"
  s3_object = BUCKET.object(cache_file)
  if s3_object.exists?
    cgi.print cgi.header({"status" => 302, "location" => s3_object.public_url})
  else
    cgi.print cgi.header({"type" => "text/plain", "status" => 404})
    cgi.print "Unknown cache file\n"
  end
else
  cgi.print cgi.header({"type" => "text/plain", "status" => 400})
  cgi.print "Unsupported command\n"
end
