FROM alexfarra/ecoforecastdocker:master
RUN R -q -e "library(devtools); install_github('khufkens/MODISTools')"
CMD ["/bin/bash", "-c", "cd actionProxy && python -u actionproxy.py"]