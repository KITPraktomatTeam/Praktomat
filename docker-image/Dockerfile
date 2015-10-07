FROM debian:wheezy

MAINTAINER Joachim Breitner <breitner@kit.edu>

RUN apt-get --yes update
RUN apt-get install --yes openjdk-7-jdk junit junit4 dejagnu gcj-jdk && apt-get clean
RUN apt-get install --yes jclassinfo && apt-get clean
RUN apt-get --purge remove --yes openjdk-6-jre-headless && apt-get clean

# R-Stuff
#RUN bash -c 'echo "deb http://cran.r-mirror.de/bin/linux/debian wheezy-cran3/" > /etc/apt/sources.list.d/r.list'
RUN bash -c 'echo "deb http://cran.uni-muenster.de/bin/linux/debian/ wheezy-cran3/" > /etc/apt/sources.list.d/r.list'
RUN apt-key adv --keyserver keys.gnupg.net --recv-key 381BA480
RUN apt-get --yes update
RUN apt-get install --yes r-base littler && apt-get clean
RUN apt-get install --yes libmysqlclient-dev && apt-get clean
RUN apt-get install --yes libxml2-dev && apt-get clean
RUN apt-get install --yes libcurl4-openssl-dev && apt-get clean
COPY Rprofile /.Rprofile
RUN Rscript -e 'install.packages("zoo", dependencies=TRUE)'
RUN Rscript -e 'install.packages("TTR", dependencies=TRUE)'
RUN Rscript -e 'install.packages("xts", dependencies=TRUE)'
RUN Rscript -e 'install.packages("quantmod", dependencies=TRUE)'
RUN Rscript -e 'install.packages("lmtest", dependencies=TRUE)'
RUN Rscript -e 'install.packages("sandwich", dependencies=TRUE)'
RUN Rscript -e 'install.packages("Rsolnp", dependencies=TRUE)'
RUN Rscript -e 'install.packages("evir", dependencies=TRUE)'
RUN Rscript -e 'install.packages("xts", dependencies=TRUE)'
RUN Rscript -e 'install.packages("fGarch", dependencies=TRUE)'
RUN Rscript -e 'install.packages("vars", dependencies=TRUE)'
RUN Rscript -e 'install.packages("moments", dependencies=TRUE)'
RUN Rscript -e 'install.packages("Ecdat", dependencies=TRUE)'

# Python-Stuff
RUN apt-get install --yes python3 python && apt-get clean
RUN apt-get install --yes python3-requests python-requests && apt-get clean
RUN apt-get install --yes python3-responses python-responses && apt-get clean
RUN apt-get install --yes python3-json python-json && apt-get clean



RUN echo "praktomat:x:1001:1001:,,,:/home/praktomat:/bin/bash" >> /etc/passwd
RUN echo "praktomat:x:1001:tester" >> /etc/group
