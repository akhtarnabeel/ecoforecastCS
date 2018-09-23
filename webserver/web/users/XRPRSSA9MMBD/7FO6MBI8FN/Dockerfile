FROM alexfarra/ecoforecastdocker:master
RUN R -q -e "install.packages('runjags', dependencies=TRUE, repos='http://cran.rstudio.com/')"
RUN R -q -e "install.packages('rjags', dependencies=TRUE, repos='http://cran.rstudio.com/')"
RUN R -q -e "install.packages('jsonlite', dependencies=TRUE, repos='http://cran.rstudio.com/')"
RUN R -q -e "library(devtools); install_github('EcoForecast/ecoforecastR')"
RUN R -q -e "library(devtools); install_github('khufkens/MODISTools')"
CMD ["/bin/bash", "-c", "cd actionProxy && python -u actionproxy.py"]