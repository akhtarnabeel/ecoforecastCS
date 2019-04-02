# EcoForecast System Setup

Following are the components that needs to be setup for running EcoForecast. 


## 1. [OpenWhisk](/SetupOpenWhisk.md)
OpenWhisk is the serverless platform that lets us run the serverless functions. 

## 2. [Webserver](/webserver/README.md)
Webserver has the user interface. We use CGI-bin for website interface.

## 3. [Database](/webserver/setup.md)
MongoDB is used to store user data. 

## 4. [ContainerMaker](/webserver/setupCM.md)
Container maker is used to create a container that has all the user specified libraries. After installing user libraries, the container is pushed to docker hub. When the serverless function runs, it gets the container from docker hub. 
