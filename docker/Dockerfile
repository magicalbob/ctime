FROM ubuntu

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

ENTRYPOINT /opt/ctime/cTime
