FROM alexfarra/ecoforecastdocker:master
RUN R -q -e "library(devtools); install_github('EcoForecast/ecoforecastR')"
CMD ["/bin/bash", "-c", "cd actionProxy && python -u actionproxy.py"]