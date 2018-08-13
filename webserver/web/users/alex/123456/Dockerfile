FROM alexfarra/ecoforecastdocker:master 
RUN R -q -e "install.packages('slidify', dependencies=TRUE, repos='http://cran.rstudio.com/')"
RUN R -q -e "library(devtools); install_github('EcoForecast/ecoforecastR')"
CMD ["/bin/bash", "-c", "cd actionProxy && python -u actionproxy.py"]