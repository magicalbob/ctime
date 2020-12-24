ctime
=====

A python program to entertain my disabled son Chris on his raspberry pi (with a touch screen monitor).

Docker
======

There's a Dockerfile, build it like this:

	docker build -t local:ctime docker

and run it like this:

	docker run -ti  -v /tmp/.X11-unix:/tmp/.X11-unix  -v ${PWD}/..:/opt/ctime -e "DISPLAY=:0" local:ctime

Currently the gui works in the docker container, but the audio doesn't and the app crashes when it tries to play music.
