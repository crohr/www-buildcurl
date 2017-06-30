# buildcurl

Precompiled software, built on demand.

## Demo

Do you need ruby-2.3.0 for debian-8, to be installed into `/usr/local`? No problem:

```
$ curl -GL buildcurl.com \
  -d recipe=ruby \
  -d version=2.3.0 \
  -d target=debian:8 \
  -d prefix=/usr/local \
  -o - | tar xzf - -C /usr/local/
```

```
$ /usr/local/bin/ruby -v
ruby 2.3.0p0 (2015-12-25 revision 53290) [x86_64-linux]
```

Perfect for Docker containers, or embedding binaries into packages, etc. It
will take some time if this is the first time a binary is built, but then it
will be cached.

See USAGE.md for more details.

## Install

Since buildcurl.com now uses the compilation service at `barebuild.com` (`ssh
barebuild.com compile ...`), this thing is just a thin wrapper to allow HTTP
access for the barebuild compilation server (instead of just through SSH).

It is installed via a debian package available at
<https://packager.io/gh/crohr/buildcurl>
