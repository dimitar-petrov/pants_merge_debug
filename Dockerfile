FROM python:3.8-bullseye 

RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
	curl \
        git \
	unzip \
	gfortran \
	docker.io \
 && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

ENTRYPOINT ["/bin/bash"]