FROM ubuntu

RUN apt-get update
RUN apt-get -y upgrade
RUN apt-get -y install python3
RUN apt-get -y install python3-pip
RUN pip3 install pytz
RUN pip3 install pyyaml
RUN pip3 install selenium
RUN pip3 install CMRESHandler
RUN pip3 install PySDL2
RUN pip3 install pygame
RUN apt-get -y install x11-apps
RUN ln -s /usr/bin/python3.8 /usr/bin/python3.6
RUN apt-get -y install libasound2
