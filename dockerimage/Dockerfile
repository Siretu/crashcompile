FROM ubuntu
MAINTAINER Erik <erikihr@gmail.com>

RUN DEBIAN_FRONTEND=noninteractive apt-get -y update

RUN DEBIAN_FRONTEND=noninteractive apt-get -y install python python-pip

RUN useradd -ms /bin/bash drone

ENV HOME /home/drone
USER drone

VOLUME ["/student.py","/test.txt"]

CMD timeout 3 cat /test.txt | python /student.py