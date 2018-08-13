FROM alexfarra/ecoforecastdocker:master
RUN R -q -e "install.packages('anomly', dependencies=TRUE, repos='http://cran.rstudio.com/')"
RUN R -q -e "install.packages('ANOM', dependencies=TRUE, repos='http://cran.rstudio.com/')"
RUN R -q -e "library(devtools); install_github('EcoForecast/ecoforecastR')"
RUN R -q -e "library(devtools); install_github('cran/AppliedPredictiveModeling')"
CMD ["/bin/bash", "-c", "cd actionProxy && python -u actionproxy.py"]