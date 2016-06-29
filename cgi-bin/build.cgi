#!/usr/bin/env ruby
require 'time'
require 'cgi'
require 'tempfile'
require 'fileutils'
require 'digest/sha1'
require 'aws-sdk'
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
S3 = Aws::S3::Resource.new
BUCKET = S3.bucket(ENV.fetch('AWS_BUCKET'))
RECIPES_DIR = File.join(SOURCE, "recipes")
EXPIRATION_DELAY = 24*3600*30
TARGETS = File.read(File.join(SOURCE, "data", "targets")).split("\n")

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
recipe_file = File.join(RECIPES_DIR, recipe || "")
request = Request.new(cgi)

available_recipes = Dir.glob(File.join(SOURCE, "recipes", "*")).select{|f| File.executable?(f)}.map{|f| File.basename(f)}
available_targets = TARGETS

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

if recipe.nil? || recipe.empty? || !File.exists?(recipe_file)
  cgi.out("status" => 400, "type" => "text/plain") do
    "Invalid recipe '#{recipe}'\n"
  end
elsif target.nil? || target.empty? || !TARGETS.include?(target)
  cgi.out("status" => 400, "type" => "text/plain") do
    <<EOF
Invalid target: #{target.inspect}
Valid targets include: #{TARGETS.map(&:inspect).join(", ")}
EOF
  end
else
  cmd = "env BUILDCURL_URL=#{ENV['BUILDCURL_URL']} SOURCE=#{SOURCE} VERSION='#{version}' PREFIX='#{prefix}' NOCACHE=#{nocache.to_s} #{SOURCE}/bin/build '#{target}' '#{recipe}'"
  fingerprint = [
    recipe,
    target.sub(":", "-"),
    version || "default",
    Digest::SHA1.hexdigest([
      target,
      recipe,
      Digest::SHA1.hexdigest(File.read(recipe_file)),
      version,
      prefix
    ].join("|"))
  ].join("_")
  cache_file = "cache/#{fingerprint}"

  if ENV['REQUEST_METHOD'] == "HEAD"
    cgi.print cgi.header({"type" => "text/plain", "status" => "302", "Location" => "/#{cache_file}.tgz", "connection" => "close"})
  elsif request.browser?
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
  elsif !nocache && BUCKET.object("#{cache_file}.tgz").exists?
    if request.sse?
      cgi.print cgi.header({"type" => "text/event-stream", "status" => "200"})
      BUCKET.object("#{cache_file}.log").get.body.each do |line|
        cgi.print "event: log\ndata: #{line}\n\n"
      end
      cgi.print "event: redirect\ndata: #{cache_file}.tgz\n\n"
    else
      cgi.print cgi.header({"type" => "text/plain", "status" => "302", "Location" => "/#{cache_file}.tgz"})
      BUCKET.object("#{cache_file}.log").get.body.each do |line|
        cgi.print line
      end
    end
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
      binfile.rewind
      logfile.rewind
      expires_at = (Time.now + EXPIRATION_DELAY)
      BUCKET.object("#{cache_file}.log").upload_file(logfile.path, acl: "public-read", expires: expires_at.httpdate, content_type: "text/plain")
      if thread.value.exitstatus == 0
        BUCKET.object("#{cache_file}.tgz").upload_file(binfile.path, acl: "public-read", expires: expires_at.httpdate, content_type: "application/x-compressed")
        cgi.print "event: redirect\ndata: #{cache_file}.tgz\n\n" if request.sse?
      end
    end
  end
end
