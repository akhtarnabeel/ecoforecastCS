# EcoForecast:
##  A Scalable and Secure Cyberinfrastructure for the Repeatability of Ecological Research

### Project Aim:
EcoForecast aims to support the ecology research by providing state of the art cloud based infrastructure facility for the ecological forecasts.

### Motivation:
Ecosystems are essential to human health and well-being, for example by protecting watersheds, pollinating agricultural crops and buffering the atmosphere against rising CO2 concentrations. Yet, these services are increasingly threatened by human activity. As the Earth rapidly moves outside the envelope of historical environmental conditions, it is increasingly urgent that the ecologists be able to provide managers and policymakers with quantitative projections that appropriately account for and quantify sources of forecast uncertainty.

### Project Aim and Overview:
This project aims to analyze and automate the procedures to make the ecological forecasts and update these forecasts over time as new data become available. To enhance access to the forecasts to other researchers, as well as to allow other researchers to 'compete' against other forecast models, we aim to build a scalable, cloud-based system for submitting, generating, archiving and disseminating multi-model ecological forecasts. Beyond advancing ecological research and socially-useful forecasts, this system will contribute to the more general development of a scalable and secure cyberinfrastructure for automated, repeatable scientific analyses applied to real-time data.

<p align="center">
<img align=center src="https://github.com/akhtarnabeel/ecoforecastCS/raw/master/screenshots/workflows.jpg" width="307.5" height="250" />
  <br> 
  Figure 1 : Examples of Ecological Workflows
</p>

#### Ecological Workflows:

Ecological workflows are composed of different prediction models, which consist of the jobs running serially or in parallel, and the output from a job is used as input to other jobs.  
Figure 1 shows examples of two such workflows. In workflow type 1, the output from job A is used by job B for the prediction, and the jobs are executed serially. In workflow type 2, the output from job A is used by job C and D for the prediction, and the job C and D are executed in parallel. 

Some jobs need to be executed periodically (e.g. every day) while other jobs are executed based on external events (e.g. new weather data). 

#### System Design:
To support ecological workflows, we create a secure and scalable cyberinfrastructure over multiple cloud providers. We use containerized approach to run ecological computations, where each job runs in a separate container. This provides the isolation and security, and help us elastically manage the resources. 

We use [Apache OpenWhisk](https://openwhisk.apache.org) for running code for ecological models. *"Apache OpenWhisk (Incubating) is an open source, distributed Serverless platform that executes functions (fx) in response to events at any scale".* In OpenWhisk, users' code runs in a container, and the container can be configured to support the environment and dependencies needed for running the code. 

<p align="center">
<img align=center src="https://github.com/akhtarnabeel/ecoforecastCS/raw/master/screenshots/System.jpg" width="700" height="500" />
  <br> 
  Figure 2 : EcoForecast System 
</p>

Our implementation of the EcoForecast is based on [Apache OpenWhisk](https://openwhisk.apache.org). We deployed the EcoForecast on GENI and Chameleon Cloud test beds. 

[GENI](http://www.geni.net) (Global Environment for Network Innovations) provides a virtual environment to run experiments. Users can reserve VMs and bare metal nodes on GENI which are located at different educational institutes and research labs across the USA. 

[Chameleon Cloud](https://www.chameleoncloud.org) is deployed at the University of Chicago and the Texas Advanced Computing Center, and it provides deeply programmable virtual resources for cloud computing experiments. Chameleon provides users access to powerful machines, that can be used for running computationally extensive tasks. 

Figure 2 shows our implementation of OpenWhisk deployment on GENI cloud edge and Chameleon cloud. 
The steps below shows the running of the system.

1. A user who wishes to run computation on EcoForecast submits the job using the web interface provided.  For running the website, we are using CGI-bin for website interface. Currently, users can only submit code in R language. Users are also given the option to chose R library that their code uses. Users can also upload supporting files, e.g. configuration files, along with their code. 

2. Code, along with supporting files, is provided to the **Orchestrator & Scheduler (O&S)**. O&S  decides where to place the *Serverless function* as Virtual Functions (VFs) for running computation for ecological research. 
Currently, VFs can run on either Chameleon Cloud or GENI nodes. 

    Chameleon has access to powerful nodes, so O&S can run serverless functions with RAM up to 8GB for each function. However, Chameleon nodes are located at one geographical location i.e. in Texas. 

    GENI nodes are spread all over the US at different educational and research institutes. However, GENI nodes have limited resources, so O&S can run serverless functions with RAM up to 2GB for each VF.

    Although VFs running on Chameleon cloud have more resources, they are bound to one geographical location. If VFs are geographically far from the data source, the download time for the input data can significantly impact the total running time of a function. Morever, saving the output from VF into a database, which is geographically far from where function executes, can also significantly impact the running time of the function. 

    Although GENI nodes have limited computation power, the functions can run at different geographical locations and VFs can be placed closer to the data source. This can reduce the download time for input data and significantly reduce the running time for the VF. 

    The O&S task is to find the perfect location for placing the VFs, either on GENI or Chameleon nodes, such that the running time is reduced and the resource requirements for VFs are fulfilled. 

3. O&S selects the node where "serverless function" will be placed as VF. Once the location is selected, O&S either creates a container image or uses one of the existing container images with all the libraries needed to run the user code. O&C then creates an OpenWhisk "action" on the selected node. Once the action is created,  O&S "invokes" the action and the code starts executing on the machine. 

4. Prediction model code that runs on OpenWhisk needs access to external data which is used as input to prediction models. A user can either upload data with the code, or the data is downloaded from different data sources as the code executes. Once the prediction is made, the output of the VF is saved in our database. Currently, we are using MongoDB for storing VF output. 

5. Once the output is saved in the database, the user can access the output using the GUI interface. 

6. Our GUI interface provides the user with different tools that can be used to understand the prediction model outputs. We used [Plotly](https://plot.ly) for plotting and comparing the output from the different prediction models.


<p align="center">
<img align=center src="https://github.com/akhtarnabeel/ecoforecastCS/raw/master/screenshots/EcoForecast.jpg" width="700" height="583" />
  <br> 
  Figure 3 : EcoForecast Architecture 
</p>




## User Manual
  
The user manual has instructions for running the system. [[link]](/UserManual.md)
  
## Setup Manual
Setup manual has instructions for setting up the system on any cloud environment.  [[link]](/SystemSetup.md)


