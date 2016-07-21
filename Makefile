all: build release
build:
	docker build -t buildcurl/buildcurl .
release:
	docker push buildcurl/buildcurl

images: build_images push_images
build_images:
	cd targets && find . -name Dockerfile -print0 | xargs -0 -n1 --max-procs=$(shell nproc) $(shell pwd)/targets/dockerize
push_images:
	cd targets && find . -name Dockerfile -print0 | xargs -0 -n1 --max-procs=$(shell nproc) $(shell pwd)/targets/push
