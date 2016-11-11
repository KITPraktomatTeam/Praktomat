FROM debian:jessie

MAINTAINER Martin Hecker <martin.hecker@kit.edu>

RUN echo "deb http://http.debian.net/debian jessie-backports main" > /etc/apt/sources.list.d/jessie-backports.list
RUN apt-get --yes update
RUN apt-get update && apt-get install -y --no-install-recommends apt-utils
RUN apt-get install --yes openjdk-8-jdk junit junit4 dejagnu gcj-jdk && apt-get clean
RUN update-java-alternatives -s java-1.8.0-openjdk


# # R-Stuff
# RUN bash -c 'echo "deb http://cran.uni-muenster.de/bin/linux/debian/ jessie-cran3/" > /etc/apt/sources.list.d/r.list'
# RUN apt-key adv --keyserver keys.gnupg.net --recv-key 381BA480
# RUN apt-get --yes update
# RUN apt-get install --yes r-base littler && apt-get clean
# RUN apt-get install --yes libmysqlclient-dev && apt-get clean
# RUN apt-get install --yes libxml2-dev && apt-get clean
# RUN apt-get install --yes libcurl4-openssl-dev && apt-get clean
# RUN apt-get install --yes ed && apt-get clean
# COPY Rprofile /.Rprofile
# RUN Rscript -e 'install.packages("zoo", dependencies=TRUE)'
# RUN Rscript -e 'install.packages("TTR", dependencies=TRUE)'
# RUN Rscript -e 'install.packages("xts", dependencies=TRUE)'
# RUN Rscript -e 'install.packages("quantmod", dependencies=TRUE)'
# RUN Rscript -e 'install.packages("lmtest", dependencies=TRUE)'
# RUN Rscript -e 'install.packages("sandwich", dependencies=TRUE)'
# RUN Rscript -e 'install.packages("Rsolnp", dependencies=TRUE)'
# RUN Rscript -e 'install.packages("evir", dependencies=TRUE)'
# RUN Rscript -e 'install.packages("xts", dependencies=TRUE)'
# RUN Rscript -e 'install.packages("fGarch", dependencies=TRUE)'
# RUN Rscript -e 'install.packages("vars", dependencies=TRUE)'
# RUN Rscript -e 'install.packages("moments", dependencies=TRUE)'
# RUN Rscript -e 'install.packages("Ecdat", dependencies=TRUE)'

# Python-Stuff
RUN apt-get update -y
RUN apt-get install --yes python3            python               && apt-get clean
RUN apt-get install --yes                    ipython              && apt-get clean
RUN apt-get install --yes python3-requests                        && apt-get clean
RUN apt-get install --yes python3-pip                             && apt-get clean
RUN apt-get install --yes python3-six        python-six           && apt-get clean
RUN apt-get install --yes python3-responses                       && apt-get clean
RUN apt-get install --yes python3-xlrd                            && apt-get clean

RUN python3 -m pip install --upgrade pip
RUN pip3 install numpy scipy matplotlib ipython pandas
RUN sed -i -e 's/^backend      : \(\(TkAgg\)\|\(tkagg\)\)$/backend      : Agg/g' /usr/local/lib/python3.4/dist-packages/matplotlib/mpl-data/matplotlibrc


RUN pip3 install statsmodels
RUN pip3 install scikit-learn
RUN pip3 install numdifftools

# Install Isabelle2016
RUN apt-get install --yes curl                                    && apt-get clean
RUN curl http://isabelle.in.tum.de/dist/Isabelle2016_app.tar.gz | tar -C /opt -xz
RUN ln -s /opt/Isabelle2016/bin/isabelle /usr/local/bin
RUN isabelle build -sbv HOL

RUN echo "praktomat:x:1001:1001:,,,:/home/praktomat:/bin/bash" >> /etc/passwd
RUN echo "praktomat:x:1001:tester" >> /etc/group

# We use a fresh tmpfs with /home in each container
RUN chmod 1777 /home
