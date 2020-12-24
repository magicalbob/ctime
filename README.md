ctime
=====

A python program to entertain my disabled son Chris on his raspberry pi (with a touch screen monitor).

Docker
======

There's a Dockerfile, build it like this:

	docker build -t local:ctime docker

and run it like this (assuming you are in docker directory):

	docker run -d  -v /tmp/.X11-unix:/tmp/.X11-unix  -v ${PWD}/..:/opt/ctime --privileged local:ctime

To exit, alt-tab back to shell and `docker rm -f $(docker ps -q)` or similar.
