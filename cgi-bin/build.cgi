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

  if !(cgi.cache_control || "").downcase.include?("no-cache") && File.exist?(cache_file)
    cgi.print cgi.header({"type" => "application/x-compressed", "status" => "OK"})
    File.open(cache_file, "r").each_line do |line|
      cgi.print line
    end
  else
    tmpfile = Tempfile.new("binary")
    Dir.mktmpdir do
      IO.popen(cmd) do |io|
        until io.eof?
          data = io.gets
          tmpfile.print data
        end
      end
    end
    tmpfile.rewind
    if $?.exitstatus == 0
      FileUtils.mv tmpfile.path, cache_file
      cgi.print cgi.header({"type" => "application/x-compressed", "status" => "OK"})
      File.open(cache_file, "r").each_line do |line|
        cgi.print line
      end
    else
      cgi.print cgi.header({"type" => "text/plain", "status" => 500})
      tmpfile.each_line do |line|
        cgi.print line
      end
    end
  end
end
