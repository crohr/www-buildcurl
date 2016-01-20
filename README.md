# buildcurl

Statically compiled software, built on demand

## Demo

Do you need ruby-2.3.0 for debian-8, to be installed into `/usr/local`? No problem:

```
curl buildcurl.com -d recipe=ruby -d version=2.3.0 -d target=debian:8 -d prefix=/usr/local -o - | tar xzf - -C /usr/local/
```

Perfect for Docker containers, or embedding binaries into packages, etc. It
will take some time if this is the first time a binary is built, but then it
will be cached.

## Install

You can install this in 5 minutes on a spare server by doing:

```bash
curl https://raw.githubusercontent.com/crohr/buildcurl/master/install.sh | sudo bash
```
