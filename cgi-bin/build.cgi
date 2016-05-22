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
RECIPES_DIR = File.join(SOURCE, "recipes")

FileUtils.mkdir_p CACHE_DIR

cgi = CGI.new
params = cgi.params

recipe = File.basename(params["recipe"].first || "")
version = params["version"].first
target = params["target"].first
prefix = params.has_key?("prefix") ? params["prefix"].first : "/usr/local"
recipe_file = File.join(RECIPES_DIR, recipe)

if recipe.nil? || target.nil?
  cgi.out("status" => 400, "type" => "text/plain") do
    File.read(File.join(SOURCE, "USAGE.md"))
  end
  exit 0
end

if recipe.nil? || recipe.empty? || !File.exists?(recipe_file)
  cgi.out("status" => 400, "type" => "text/plain") do
    "Invalid recipe '#{recipe}'\n"
  end
elsif target.nil? || target.empty?
  cgi.out("status" => 400, "type" => "text/plain") do
    "Invalid target '#{target}'\n"
  end
else
  cmd = "env BUILDCURL_URL=#{ENV['BUILDCURL_URL']} SOURCE=#{SOURCE} VERSION='#{version}' PREFIX='#{prefix}' #{SOURCE}/bin/build '#{target}' '#{recipe}'"
  # TODO: include md5sum of recipe file in fingerprint
  fingerprint = Digest::SHA1.hexdigest [
    target,
    recipe,
    Digest::SHA1.hexdigest(File.read(recipe_file)),
    version,
    prefix
  ].join("|")
  cache_file = File.join(CACHE_DIR, fingerprint)

  if ENV['REQUEST_METHOD'] == "HEAD"
    cgi.print cgi.header({"type" => "text/plain", "status" => "302", "location" => "/cache/#{fingerprint}.tgz", "connection" => "close"})
  elsif !(cgi.cache_control || "").downcase.include?("no-cache") && File.exist?("#{cache_file}.tgz")
    cgi.print cgi.header({"type" => "text/plain", "status" => "302", "location" => "/cache/#{fingerprint}.tgz"})
    File.open("#{cache_file}.log", "r").each_line do |line|
      cgi.print line
    end
  else
    STDOUT.sync = true
    cgi.print cgi.header({"type" => "text/plain", "status" => "302", "location" => "/cache/#{fingerprint}.tgz"})
    require 'open3'
    data = {:out => [], :err => []}
    binfile = Tempfile.new("binary")
    logfile = Tempfile.new("log")
    Open3.popen3(cmd) do |stdin, stdout, stderr, thread|
      # read each stream from a new thread
      stream_threads = []
      { :out => stdout, :err => stderr }.each do |key, stream|
        stream_threads << Thread.new do
          until (raw_line = stream.gets).nil? do
            if key == :out
              binfile.print raw_line
            else
              logfile.print raw_line
              cgi.print raw_line
            end
          end
        end
      end

      thread.join # don't exit until the external process is done
      stream_threads.each(&:join)
      binfile.rewind
      logfile.rewind
      FileUtils.mv logfile.path, "#{cache_file}.log"
      if thread.value.exitstatus == 0
        FileUtils.mv binfile.path, "#{cache_file}.tgz"
      end
    end
  end
end
