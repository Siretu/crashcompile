FROM ubuntu
MAINTAINER Erik <erikihr@gmail.com>

RUN DEBIAN_FRONTEND=noninteractive apt-get -y update

RUN DEBIAN_FRONTEND=noninteractive apt-get -y install python python-pip

VOLUME ["/student.py","/test.txt"]

CMD cat /test.txt | python /student.py