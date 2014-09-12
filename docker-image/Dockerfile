FROM debian:wheezy

MAINTAINER Joachim Breitner <breitner@kit.edu>

RUN apt-get --yes update
RUN apt-get install --yes openjdk-7-jdk junit junit4 dejagnu gcj-jdk; apt-get clean
RUN apt-get install --yes jclassinfo ; apt-get clean
RUN apt-get --purge remove --yes openjdk-6-jre-headless; apt-get clean
RUN apt-get install --yes r-base ; apt-get clean

RUN echo "praktomat:x:1001:1001:,,,:/home/praktomat:/bin/bash" >> /etc/passwd
RUN echo "praktomat:x:1001:tester" >> /etc/group
