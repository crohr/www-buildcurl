#!/usr/bin/env ruby
require 'securerandom'
require 'time'
require 'cgi'
require 'tempfile'
require 'fileutils'
require 'dotenv'
require 'open3'
require 'logger'
require 'erb'

class Request
  attr_reader :cgi
  def initialize(cgi)
    @cgi = cgi
    @sse = (cgi.accept || "").include?("text/event-stream")
    @browser = (cgi.accept || "").include?("text/html")
  end

  def sse? ; @sse ; end
  def browser? ; @browser ; end
end

SOURCE = ENV.fetch('SOURCE') { File.dirname(Dir.pwd) }
Dotenv.load File.join(SOURCE, ".env")

STDOUT.sync = true
STDERR.sync = true
logger = Logger.new(STDERR)
cgi = CGI.new
params = cgi.params

recipe = params["recipe"].first
version = params["version"].first
target = params["target"].first
prefix = params["prefix"].first
prefix = "/usr/local" if prefix.nil? || prefix.empty? 
nocache = params["nocache"].first == "true"
request = Request.new(cgi)

available_targets = File.read(File.join(SOURCE, "data", "targets")).split("\n")
available_recipes = File.read(File.join(SOURCE, "data", "recipes")).split("\n")

if recipe.nil? || target.nil?
  if request.browser?
    cgi.print cgi.header({"type" => "text/html", "status" => "200"})
    cgi.print File.read("#{SOURCE}/header.html")
    cgi.print ERB.new(File.read("#{SOURCE}/_form.html")).result
    cgi.print %x{markdown #{File.join(SOURCE, "USAGE.md")}}
    cgi.print File.read("#{SOURCE}/footer.html")
  else
    cgi.out("status" => 400, "type" => "text/plain") do
      File.read(File.join(SOURCE, "USAGE.md"))
    end
  end
  exit 0
end

if recipe.nil? || recipe.empty?
  cgi.out("status" => 400, "type" => "text/plain") do
    "Invalid recipe '#{recipe}'\n"
  end
elsif target.nil? || target.empty?
  cgi.out("status" => 400, "type" => "text/plain") do
    <<EOF
Invalid target: #{target.inspect}
EOF
  end
else
  cmd = %{ssh -q -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null barebuild.com \
    "compile '#{recipe}' --target='#{target}' --prefix='#{prefix}' --version='#{version}' #{'--no-cache' if nocache}"}
  fingerprint = SecureRandom.uuid
  cache_file = "cache/#{fingerprint}"

  if request.browser?
    cgi.print cgi.header({"type" => "text/html", "status" => "200"})
    cgi.print File.read("#{SOURCE}/header.html")
    cgi.print ERB.new(File.read("#{SOURCE}/_form.html")).result
    cgi.print "<div class=spinner id=spinner></div>"
    cgi.print "<h1 class=monospace>Building #{recipe} #{version} #{target} #{prefix}...</h1>"
    cgi.print "<div id=logs></div><div id=link class=hidden>Download <a href=/cache/#{fingerprint}.tgz>#{fingerprint}.tgz</a></div>"
    cgi.print <<EOF
    <script>
    var autoscroll = true;
    var src = new EventSource("/?recipe=#{recipe}&target=#{target}&version=#{version}&prefix=#{prefix}&nocache=#{nocache.to_s}");
    src.onerror = function() {
      src.close();
      document.getElementById("spinner").className += " hidden";
    }
    document.body.onscroll = function() {
      autoscroll = false;
      if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight) {
        autoscroll = true;
      }
    }
    src.addEventListener("log", function(e) {
      var newElement = document.createElement("p");
      newElement.innerHTML = e.data;
      setTimeout(function() {
        document.getElementById("logs").appendChild(newElement);
        if (autoscroll) { window.scrollTo(0,document.body.scrollHeight); }
      }, 10);
    });
    src.addEventListener("redirect", function(e) {
      src.close();
      setTimeout(function() {
        document.getElementById("spinner").className += " hidden";
        document.getElementById("link").className = "";
        if (autoscroll) { window.scrollTo(0,document.body.scrollHeight); }
        window.location.href = e.data;
      }, 100);
    });
    </script>
EOF
    cgi.print File.read("#{SOURCE}/footer.html")
  else
    if request.sse?
      cgi.print cgi.header({"type" => "text/event-stream", "status" => "200"})
    else
      cgi.print cgi.header({"type" => "text/plain", "status" => "302", "Location" => "/#{cache_file}.tgz"})
    end
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
              if request.sse?
                cgi.print "event: log\ndata: #{raw_line}\n\n"
              else
                cgi.print raw_line
              end
            end
          end
        end
      end

      thread.join # don't exit until the external process is done
      stream_threads.each(&:join)
      binfile.close
      logfile.close
      FileUtils.cp(binfile.path, "/tmp/#{fingerprint}.tgz", verbose: true)
      if thread.value.exitstatus == 0
        cgi.print "event: redirect\ndata: #{cache_file}.tgz\n\n" if request.sse?
      end
    end
  end
end
