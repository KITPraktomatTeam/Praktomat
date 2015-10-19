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
RUN echo deb http://http.debian.net/debian wheezy-backports main > /etc/apt/sources.list.d/wheezy-backports.list
RUN apt-get update -y
RUN apt-get install --yes python3 python && apt-get clean
RUN apt-get install --yes python3-requests python-requests && apt-get clean
RUN apt-get install --yes python3-pip python-pip && apt-get clean
RUN apt-get install --yes -t wheezy-backports python-six python3-six && apt-get clean
RUN apt-get install --yes -t wheezy-backports ipython ipython3 && apt-get clean
RUN apt-get install --yes python-numpy && apt-get clean
RUN apt-get install --yes python-scipy && apt-get clean
RUN apt-get install --yes python-pandas && apt-get clean
RUN apt-get install --yes python-matplotlib && apt-get clean
RUN pip install --upgrade setuptools==18.3.1
RUN pip install responses
RUN pip-3.2 install --upgrade pip
RUN /usr/local/bin/pip3.2 install --upgrade setuptools==18.3.1
RUN /usr/local/bin/pip3.2 install numpy
RUN /usr/local/bin/pip3.2 install scipy
RUN /usr/local/bin/pip3.2 install pandas
RUN apt-get install --yes libfreetype6-dev && apt-get clean
RUN /usr/local/bin/pip3.2 install matplotlib
RUN /usr/local/bin/pip3.2 install responses
RUN /usr/local/bin/pip3.2 install statsmodels
RUN /usr/local/bin/pip3.2 install scikit-learn



RUN echo "praktomat:x:1001:1001:,,,:/home/praktomat:/bin/bash" >> /etc/passwd
RUN echo "praktomat:x:1001:tester" >> /etc/group
