#!/usr/bin/env ruby

require 'webrick'

server = WEBrick::HTTPServer.new :Port => 1234
server.mount "/", WEBrick::HTTPServlet::FileHandler, File.expand_path("../cgi-bin/", __FILE__)
trap('INT') { server.stop }
server.start
