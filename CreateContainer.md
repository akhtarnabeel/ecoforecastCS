# Creating your own Docker container to execute your code on:

# Install Docker:
- You can use this link to install Docker from its official source on whatever OS you're running: https://docs.docker.com/install/

# Create a Dockerhub account:
- You can create one here: https://hub.docker.com/ if you don't already have one
- Create a repo for your project, each repo can have multiple tags (or multiple containers) under the same repo. So you can make one repo for multiple different container with different dependencies. The IMAGE_ID will differentiate them.

# Log in from the CLI:
- Run: 
```
docker login --username=yourusername --password=yourpassword
```

# Creating your container:
- Create a file called "Dockerfile"
- The contents of the file should look like this: 
```
# This line imports our base image
FROM alexfarra/ecoforecastdocker:master

# This line is a comment
# Insert your commands to install packages here
# You can install as many as you want in a row
# An example of installing the R package ggplot2:
RUN R -q -e "install.packages('ggplot2', repos='http://cran.rstudio.com/')"

# These lines are needed for OpenWhisk
RUN rm -rf /tmp/*
CMD ["/bin/bash", "-c", "cd actionProxy && python -u actionproxy.py"]
```

# Build and push your container:
- Build the container by running:
```
Docker build -t DOCKERHUB_USERNAME/DOCKERHUB_REPO:IMAGE_TAG path/to/Dockerfile
```
For example, if you're in the same directory as your Dockerfile and your Dockerhub username is alexfarra and your repo that your pushing to is myecoforecastcontainer you can just run:
```
Docker build -t alexfarra/myecoforecastcontainer:experiment1 .
```
- Push the container by running:
```
Docker push DOCKERHUB_USERNAME/DOCKERHUB_REPO:IMAGE_TAG
```
So with the same example again we would get:
```
Docker push alexfarra/myecoforecastcontainer:experiment1
```
