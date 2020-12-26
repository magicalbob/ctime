FROM ubuntu

ENV DISPLAY=:0

RUN apt-get update \
 && apt-get -y upgrade \
 && apt-get -y install python3 \
 && apt-get -y install python3-pip \
 && pip3 install pytz \
 && pip3 install pyyaml \
 && pip3 install selenium \
 && pip3 install CMRESHandler \
 && pip3 install PySDL2 \
 && pip3 install pygame \
 && apt-get -y install x11-apps \
 && ln -s /usr/bin/python3.8 /usr/bin/python3.6 \
 && apt-get -y install libasound2
RUN ln -fs /usr/share/zoneinfo/Europe/London /etc/localtime
RUN export DEBIAN_FRONTEND=noninteractive
RUN apt-get install -y tzdata
RUN apt-get -y install firefox

ENTRYPOINT /opt/ctime/cTime
