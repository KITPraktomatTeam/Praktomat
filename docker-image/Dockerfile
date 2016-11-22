FROM debian:jessie
#FROM mikemckibben/java:1.8
#FROM java:8
FROM openjdk:8-jdk

MAINTAINER Joachim Breitner <breitner@kit.edu>

RUN echo "deb http://http.debian.net/debian jessie-backports main" > /etc/apt/sources.list.d/jessie-backports.list
RUN apt-get --yes update
RUN apt-get install --yes openjdk-8-jdk junit junit4 dejagnu gcj-jdk && apt-get clean
RUN update-java-alternatives -s java-1.8.0-openjdk

# Python-Stuff
RUN apt-get update -y
RUN apt-get install --yes python3            python               && apt-get clean
RUN apt-get install --yes ipython3           ipython              && apt-get clean
RUN apt-get install --yes python3-requests                        && apt-get clean
RUN apt-get install --yes python3-pip                             && apt-get clean
RUN apt-get install --yes python3-six        python-six           && apt-get clean
RUN apt-get install --yes python3-numpy                           && apt-get clean
RUN apt-get install --yes python3-scipy                           && apt-get clean
RUN apt-get install --yes python3-pandas                          && apt-get clean

RUN apt-get install --yes python3-matplotlib                      && apt-get clean
RUN sed -i -e 's/^backend      : TkAgg$/backend      : Agg/g' /etc/matplotlibrc

RUN apt-get install --yes python3-responses                       && apt-get clean
RUN apt-get install --yes python3-xlrd                            && apt-get clean

# Requirements for statsmodels
RUN apt-get install --yes python3-patsy                           && apt-get clean

RUN pip3 install statsmodels
RUN pip3 install scikit-learn

# more recent versions of numdifftools pull a whole lot of newer versions of other packages than those already installed from the debian packages (numpy, scipy), we don't want that
RUN pip3 install numdifftools==0.7.7

# Install Isabelle2016
RUN apt-get install --yes curl                                    && apt-get clean
RUN curl http://isabelle.in.tum.de/dist/Isabelle2016_app.tar.gz | tar -C /opt -xz
RUN ln -s /opt/Isabelle2016/bin/isabelle /usr/local/bin
RUN isabelle build -sbv HOL



###################SCALA###################

ENV SCALA_VERSION 2.11.7
ENV SBT_VERSION 0.13.12

ENV SBT_OPTS -Xmx2G -XX:+UseConcMarkSweepGC -XX:+CMSClassUnloadingEnabled -Xss2M -Duser.timezone=GMT

# install sbt
RUN wget https://dl.bintray.com/sbt/debian/sbt-$SBT_VERSION.deb
RUN dpkg -i sbt-$SBT_VERSION.deb

# install scala
RUN wget https://downloads.typesafe.com/scala/$SCALA_VERSION/scala-$SCALA_VERSION.deb
RUN dpkg -i scala-$SCALA_VERSION.deb

RUN sbt

#########################################

RUN echo "praktomat:x:1001:1001:,,,:/home/praktomat:/bin/bash" >> /etc/passwd
RUN echo "praktomat:x:1001:tester" >> /etc/group

# We use a fresh tmpfs with /home in each container
RUN chmod 1777 /home