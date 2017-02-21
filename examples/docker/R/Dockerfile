# R-Stuff
RUN bash -c 'echo "deb http://cran.uni-muenster.de/bin/linux/debian/ jessie-cran3/" > /etc/apt/sources.list.d/r.list'
RUN apt-key adv --keyserver keys.gnupg.net --recv-key 381BA480
RUN apt-get --yes update
RUN apt-get install --yes r-base littler && apt-get clean
RUN apt-get install --yes libmysqlclient-dev && apt-get clean
RUN apt-get install --yes libxml2-dev && apt-get clean
RUN apt-get install --yes libcurl4-openssl-dev && apt-get clean
RUN apt-get install --yes ed && apt-get clean
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
