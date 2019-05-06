#!/usr/bin/env ruby

require 'webrick'

server = WEBrick::HTTPServer.new :Port => ENV.fetch('PORT') { 1234 }.to_i, :BindAddress => ENV.fetch('BIND') { "0.0.0.0" }
server.mount "/", WEBrick::HTTPServlet::FileHandler, File.expand_path("../cgi-bin/build.cgi", __FILE__)
trap('INT') { server.stop }
server.start
