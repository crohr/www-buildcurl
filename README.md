# buildcurl

Statically compiled software, built on demand

## Demo

Do you need ruby-2.3.0 for debian-8, to be installed into `/usr/local`? No problem:

```
$ curl buildcurl.com \
  -d recipe=ruby \
  -d version=2.3.0 \
  -d target=debian:8 \
  -d prefix=/usr/local \
  -o - | tar xzf - -C /usr/local/
```

```
$ ruby -v
ruby 2.3.0p0 (2015-12-25 revision 53290) [x86_64-linux]
```

Perfect for Docker containers, or embedding binaries into packages, etc. It
will take some time if this is the first time a binary is built, but then it
will be cached.

## Install

docker run -d --name buildcurl -p 80:80 -v /var/run/docker.sock:/var/run/docker.sock \
  -e AWS_ACCESS_KEY_ID=key \
  -e AWS_SECRET_ACCESS_KEY=secret \
  -e AWS_REGION=us-east-1 \
  -e AWS_BUCKET=cache.example.com \
  -e BUILDCURL_URL=http://example.com:80 \
  buildcurl/buildcurl
