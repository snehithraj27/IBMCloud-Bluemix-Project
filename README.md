# IBMCloud-Bluemix-Project
Allow users to find out (query) interesting information about earthquakes.

Description: 
This project provides a local interface to a cloud service that will allow a user to upload earthquake data and   
investigate it. 

For input data Please go to:
https://earthquake.usgs.gov/earthquakes/feed/v1.0/csv.php 

and get all earth quakes for the last 30 days (bottom right), a .csv file, 
place these on the cloud service provider and import this into SQL.  

The cloud-based “service” will allow a user to: 
 - Search for and count all earthquakes that occurred with a magnitude greater  
  than 5.0 
 - Search for 2.0 to 2.5, 2.5 to 3.0… for a week a day or the whole 30 days. 
 - Find earthquakes that were near (20 km, 50 km?) of a specified location. 
 - Find clusters of earthquakes 
 - Do large (>4.0 mag) occur more often at night? 
