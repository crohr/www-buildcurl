# BUILDCURL.com

Build static binaries on demand.

## Usage

    curl buildcurl.com --get \
        -d recipe=RECIPE \
        -d target=TARGET \
        -d version=VERSION \
        -d prefix=PREFIX \
        -o output.tgz

`version` and `prefix` are optional. `version` will default to whatever default
version is specified in the `recipe`, and `prefix` defaults to `/usr/local`.

## Supported targets

* ubuntu:16.04
* ubuntu:14.04
* ubuntu:12.04
* debian:8
* debian:7
* el:6 (CentOS / RHEL 6.x)
* el:7 (CentOS / RHEL 7.x)
* sles:12
* sles:11
* fedora:20

## Supported recipes

See <https://github.com/crohr/buildcurl/tree/master/recipes>.

## Example

Install ruby-2.3.0 for ubuntu:14.04 into /usr/local:

    curl buildcurl.com --get -d recipe=ruby -d target=ubuntu:14.04 -d version=2.3.0 -d prefix=/usr/local | tar xzf - -C /usr/local

    /usr/local/bin/ruby -v
    #=> ruby 2.3.1p112 (2016-04-26 revision 54768) [x86_64-linux]

    /usr/local/bin/gem -v
    #=> 2.5.1

## Tips

### Display build log on error

The build log is sent as output if the build fails, so you can just check
whether the output is a valid gzip file, and display it if that's not the case:

    curl buildcurl.com --get -d recipe=ruby -d target=ubuntu:14.04 -d version=2.3.0 -d prefix=/usr/local -o output.tgz && \
      gunzip -t ouput.tgz || ( cat output.tgz && exit 1 )

More details at <https://github.com/crohr/buildcurl>.
