#!/usr/bin/env ruby
require 'time'
require 'cgi'
require 'tempfile'
require 'fileutils'
require 'digest/sha1'
require 'aws-sdk'
require 'dotenv'
require 'open3'

SOURCE = ENV.fetch('SOURCE') { File.dirname(Dir.pwd) }
Dir.chdir(SOURCE) { Dotenv.load }
S3 = Aws::S3::Resource.new
BUCKET = S3.bucket(ENV.fetch('AWS_BUCKET'))
RECIPES_DIR = File.join(SOURCE, "recipes")
EXPIRATION_DELAY = 24*3600*30

cgi = CGI.new
params = cgi.params

recipe = File.basename(params["recipe"].first || "")
version = params["version"].first
target = params["target"].first
prefix = params["prefix"].first
prefix = "/usr/local" if prefix.nil? || prefix.empty? 
nocache = params["nocache"].first == "true"
recipe_file = File.join(RECIPES_DIR, recipe)

if recipe.nil? || target.nil?
  if (cgi.accept || "").include?("text/html")
    cgi.print cgi.header({"type" => "text/html", "status" => "200"})
    cgi.print <<EOF
<html><head>
  <title>buildcurl</title>
  <style>
    body{margin:1.5em 1em;}
    .input{display:inline-block;margin-right:1em;font-family:monospace;font-size:10px;}
    .input label{margin-right:.5em;}
  </style>
  </head><body>
EOF
    cgi.print "<form action=/ method=get>"
    cgi.print "<div class=input><label for=recipe>Recipe:</label><select name=recipe>#{Dir.glob(File.join(SOURCE, "recipes", "*")).select{|f| File.executable?(f)}.map{|t| File.basename(t)}.sort.map{|t| "<option value=#{t} #{"selected" if t == "ruby"}>#{t}</option>"}}</select></div>"
    cgi.print "<div class=input><label for=version>Version:</label><input type=text name=version placeholder=2.1.3></div>"
    cgi.print "<div class=input><label for=target>Target:</label><select name=target>#{File.read(File.join(SOURCE, "data", "targets")).split("\n").map{|t| "<option value=#{t}>#{t}</option>"}}</select></div>"
    cgi.print "<div class=input><label for=prefix>Prefix:</label><input type=text name=prefix placeholder=/usr/local></div>"
    cgi.print "<input type=submit value=BUILD>"
    cgi.print "</form>"
    cgi.print %x{markdown #{File.join(SOURCE, "USAGE.md")}}
    cgi.print "</body></html>"
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
elsif target.nil? || target.empty?
  cgi.out("status" => 400, "type" => "text/plain") do
    "Invalid target '#{target}'\n"
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
  elsif cgi.accept.include?("text/html")
    cgi.print cgi.header({"type" => "text/html", "status" => "200"})
    cgi.print "<html><head>"
    cgi.print <<EOF
    <style>
      body{font-family: monospace;margin-bottom:2em;}
      #logs p{margin:0}
      #spinner{position:fixed;right:1em;top:1em;}
      .hidden{display:none;}
      .spinner {
        width: 2em;
        height: 2em;
        background-color: #333;
        -webkit-animation: sk-rotateplane 1.2s infinite ease-in-out;
        animation: sk-rotateplane 1.2s infinite ease-in-out;
      }

      @-webkit-keyframes sk-rotateplane {
        0% { -webkit-transform: perspective(120px) }
        50% { -webkit-transform: perspective(120px) rotateY(180deg) }
        100% { -webkit-transform: perspective(120px) rotateY(180deg)  rotateX(180deg) }
      }

      @keyframes sk-rotateplane {
        0% { 
          transform: perspective(120px) rotateX(0deg) rotateY(0deg);
          -webkit-transform: perspective(120px) rotateX(0deg) rotateY(0deg) 
        } 50% { 
          transform: perspective(120px) rotateX(-180.1deg) rotateY(0deg);
          -webkit-transform: perspective(120px) rotateX(-180.1deg) rotateY(0deg) 
        } 100% { 
          transform: perspective(120px) rotateX(-180deg) rotateY(-179.9deg);
          -webkit-transform: perspective(120px) rotateX(-180deg) rotateY(-179.9deg);
        }
      }
    </style>
EOF
    cgi.print "</head><body><div class=spinner id=spinner></div>"
    cgi.print "<h1>#{recipe} #{version} #{target} #{prefix}</h1>"
    cgi.print "<div id=logs></div><div id=link class=hidden>Download <a href=/cache/#{fingerprint}.tgz>#{fingerprint}.tgz</a></div>"
    cgi.print <<EOF
    <script>
    var autoscroll = true;
    var src = new EventSource("/?recipe=#{recipe}&target=#{target}&version=#{version}&prefix=#{prefix}&nocache=#{nocache.to_s}");
    src.onerror = function() { console.log("error"); src.close();}
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
    cgi.print "</body></html>"
  elsif !nocache && BUCKET.object("#{cache_file}.tgz").exists?
    STDOUT.sync = true
    if cgi.accept.include?("text/event-stream")
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
    STDOUT.sync = true
    if cgi.accept.include?("text/event-stream")
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
              if cgi.accept.include?("text/event-stream")
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
        cgi.print "event: redirect\ndata: #{cache_file}.tgz\n\n"
      end
    end
  end
end
