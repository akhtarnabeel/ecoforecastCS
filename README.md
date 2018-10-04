# EcoForecast:
##  A Scalable and Secure Cyberinfrastructure for the Repeatability of Ecological Research

### Project Aim:
EcoForecast aims to support ecology research by providing state of the art cloud based infrastructure facility for the ecological forecasts.

### Motivation:
Ecosystems are essential to human health and well-being, for example by protecting watersheds, pollinating agricultural crops and buffering the atmosphere against rising CO2 concentrations. Yet, these services are increasingly threatened by human activity. As the Earth rapidly moves outside the envelope of historical environmental conditions, it is increasingly urgent that ecologists be able to provide managers and policymakers with quantitative projections that appropriately account for and quantify sources of forecast uncertainty.

### Project Overview:
This projects aim to analyze and automate procedures to make ecological forecasts and update these forecasts over time as new data become available. To enhance access to the forecasts to other researchers, as well as to allow other researchers to 'compete' against other forecast models, we aim to build a scalable, cloud-based system for submitting, generating, archiving and disseminating multi-model ecological forecasts. Beyond advancing ecological research and socially-useful forecasts, this system will contribute to the more general development of a scalable and secure cyberinfrastructure for automated, repeatable scientific analyses applied to real-time data.

<p align="center">
<img align=center src="https://github.com/akhtarnabeel/ecoforecastCS/raw/master/screenshots/workflows.jpg" width="307.5" height="250" />
  <br> 
  Figure 1 : Examples of Ecological Workflows
</p>

#### Ecological Workflows:

Ecological workflows are composed of different prediction models, which consist of the jobs running serially or in parallel, and the output from a job is used as input to other jobs.  
Figure 1 shows examples of two such workflows. In workflow type 1, the output from job A is used by job B for the prediction, and the jobs are executed serially. In workflow type 2, the output from job A is used by job C and D for the prediction, and the job C and D are executed in parallel. 

Some jobs need to be executed periodically (e.g. every day) while other jobs are executed based on external events (e.g. new weather data). 

To support ecological workflows, we aim to created a secure and scalable cyberinfrastructure over multiple cloud providers.

<p align="center">
<img align=center src="https://github.com/akhtarnabeel/ecoforecastCS/raw/master/screenshots/System.jpg" width="700" height="500" />
  <br> 
  Figure 2 : EcoForecast System 
</p>

## User Manual
  [link](/UserManual.md)
  
  
## Setup Manual
  [link](/SystemSetup.md)
