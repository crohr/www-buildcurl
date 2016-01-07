#!/usr/bin/env ruby
require 'time'
require 'cgi'
require 'tempfile'
require 'fileutils'

require 'cgi'

SOURCE = ENV.fetch('SOURCE') { File.dirname(Dir.pwd) }

tmpdir = Dir.mktmpdir
cgi = CGI.new
params = cgi.params

recipe = File.basename(params["recipe"].first || "")
version = params["version"].first
target = params["target"].first
prefix = params.has_key?("prefix") ? params["prefix"].first : "/app/.heroku/#{recipe}"

if recipe.nil? || recipe.empty?
  cgi.out("status" => 400) do
    "Invalid recipe '#{recipe}'\n"
  end
elsif target.nil? || target.empty?
  cgi.out("status" => 400) do
    "Invalid target '#{target}'\n"
  end
else
  cmd = "env SOURCE=#{SOURCE} VERSION='#{version}' PREFIX='#{prefix}' #{SOURCE}/bin/build '#{target}' '#{recipe}'"

  Dir.chdir tmpdir
  cgi.print cgi.header({"type" => "application/x-compressed", "status" => "OK"})
  IO.popen(cmd) do |io|
    until io.eof?
    data = io.gets
    cgi.print data
    end
  end
  FileUtils.rm_rf tmpdir
end
