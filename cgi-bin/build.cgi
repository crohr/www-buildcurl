#!/usr/bin/env ruby
require 'time'
require 'cgi'
require 'tempfile'
require 'fileutils'
require 'digest/sha1'

require 'cgi'

SOURCE = ENV.fetch('SOURCE') { File.dirname(Dir.pwd) }
File.read(File.join(SOURCE, ".env")).each_line do |line|
  k, v = line.chomp.split("=", 2)
  ENV[k] = v
end
CACHE_DIR = ENV.fetch('CACHE_DIR') { File.join(SOURCE, "cache") }
FileUtils.mkdir_p CACHE_DIR

cgi = CGI.new
params = cgi.params

recipe = File.basename(params["recipe"].first || "")
version = params["version"].first
target = params["target"].first
prefix = params.has_key?("prefix") ? params["prefix"].first : "/usr/local"

if recipe.nil? || recipe.empty?
  cgi.out("status" => 400) do
    "Invalid recipe '#{recipe}'\n"
  end
elsif target.nil? || target.empty?
  cgi.out("status" => 400) do
    "Invalid target '#{target}'\n"
  end
else
  cmd = "env BUILDCURL_URL=#{ENV['BUILDCURL_URL']} SOURCE=#{SOURCE} VERSION='#{version}' PREFIX='#{prefix}' #{SOURCE}/bin/build '#{target}' '#{recipe}'"
  # TODO: include md5sum of recipe file in fingerprint
  fingerprint = Digest::SHA1.hexdigest [target, recipe, version, prefix].join("|")
  cache_file = File.join(CACHE_DIR, fingerprint)

  if File.exist?(cache_file)
    cgi.print cgi.header({"type" => "application/x-compressed", "status" => "OK"})
    File.open(cache_file, "r").each_line do |line|
      cgi.print line
    end
  else
    tmpfile = Tempfile.new("binary")
    Dir.mktmpdir do
      cgi.print cgi.header({"type" => "application/x-compressed", "status" => "OK"})
      IO.popen(cmd) do |io|
        until io.eof?
          data = io.gets
          cgi.print data
          tmpfile.print data
        end
      end
      if $?.exitstatus == 0
        FileUtils.mv tmpfile.path, cache_file
      end
    end
  end
end
