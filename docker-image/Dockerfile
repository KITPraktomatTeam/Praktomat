FROM debian:buster

MAINTAINER Simon Bischof <simon.bischof@kit.edu>

# set up new user
RUN echo "praktomat:x:1001:1001:,,,:/home/praktomat:/bin/bash" >> /etc/passwd
RUN echo "praktomat:x:1001:tester" >> /etc/group

# We use a fresh tmpfs with /home in each container
RUN chmod 1777 /home

RUN apt-get --yes update
RUN apt-get update && apt-get install -y --no-install-recommends apt-utils
RUN apt-get install --yes ca-certificates-java
RUN apt-get install --yes openjdk-11-jdk junit junit4 && apt-get clean
# java 11 is already the default version
#RUN update-java-alternatives -s java-1.11.0-openjdk-amd64

# Python-Stuff
RUN apt-get update -y
RUN apt-get install --yes python3            python               && apt-get clean
RUN apt-get install --yes                    ipython              && apt-get clean
RUN apt-get install --yes python3-requests                        && apt-get clean
RUN apt-get install --yes python3-pip                             && apt-get clean
RUN apt-get install --yes python3-six        python-six           && apt-get clean
RUN apt-get install --yes python3-responses                       && apt-get clean
RUN apt-get install --yes python3-xlrd                            && apt-get clean
RUN apt-get install --yes python3-simplejson python-simplejson    && apt-get clean


################ISABELLE#################
# Install Isabelle2019
RUN apt-get install --yes curl libc6-i386 lib32stdc++6  && apt-get clean
RUN curl https://isabelle.in.tum.de/website-Isabelle2019/dist/Isabelle2019_linux.tar.gz | tar -C /opt -xz
RUN ln -s /opt/Isabelle2019/bin/isabelle /usr/local/bin
RUN isabelle build -bv HOL
#########################################


###################SCALA###################
# needs to be enabled if the Scala Checker is used
#RUN apt-get install --yes wget && apt-get clean

#ENV SCALA_VERSION 2.11.7
#ENV SBT_VERSION 0.13.12

#ENV SBT_OPTS -Xmx2G -XX:+UseConcMarkSweepGC -XX:+CMSClassUnloadingEnabled -Xss2M -Duser.timezone=GMT

# install sbt
#RUN wget https://dl.bintray.com/sbt/debian/sbt-$SBT_VERSION.deb
#RUN dpkg -i sbt-$SBT_VERSION.deb

# install scala
#RUN wget https://downloads.typesafe.com/scala/$SCALA_VERSION/scala-$SCALA_VERSION.deb
#RUN dpkg -i scala-$SCALA_VERSION.deb

#RUN sbt

#########################################


###################GHC###################

RUN apt-get install --yes ghc libghc-test-framework-dev libghc-test-framework-hunit-dev libghc-test-framework-quickcheck2-dev

#########################################
