FROM centos:7

ENV DISPLAY=:0

RUN yum -y install python3 \
 && yum -y install python3-pip \
 && pip3 install pytz \
 && pip3 install pyyaml \
 && pip3 install selenium \
 && pip3 install CMRESHandler \
 && pip3 install PySDL2 \
 && pip3 install pygame \
 && yum -y install xorg-x11-apps \
 && yum -y install alsa-lib \
 && ln -fs /usr/share/zoneinfo/Europe/London /etc/localtime \
 && yum install -y tzdata \
 && yum -y install firefox \
 && yum install -y chrome-gnome-shell

ENTRYPOINT /opt/ctime/cTime
