# test-univ_db
This Repository for Ingestion Data from CSV

The output is **report_attendance.csv**

for run this script need instal docker and docker desktop (_if u need UI_), trhid apps for query database, and python3 (_if want testing outside docker_).
In this case, using database postgresql (_pull images by docker_).

For the first step, pull this repo into your local machine and then go to that folder from terminal/command line

<img width="1053" alt="image" src="https://user-images.githubusercontent.com/42090252/163710555-3e72e214-6403-4fbb-b4a3-73dcc9d64697.png">
<img width="1049" alt="image" src="https://user-images.githubusercontent.com/42090252/163710597-75f93dcc-5a22-440a-b03d-647f56bc6d2e.png">

cmd : **docker-compose up -d**__ -> for up docker compose in background
for check the docker container is up, can check with **docker ps**__ or docker container ls -a and for the images _**docker images**_. Or also can check in docker desktop

<img width="838" alt="image" src="https://user-images.githubusercontent.com/42090252/163711305-39666d73-6337-40e0-8e9b-e43719036c79.png">


Acctually this script handle for the all script run after _**docker-compose up**_ but sometimes if there status error or exited(1), for the make sure that can execute this cmd docker run <images name>, for step by step in order, and in this case :
  -  docker run test-univ_db_source_to_raw_layer
  -  docker run test-univ_db_raw_layer_to_dataset
  -  docker run test-univ_db_dataset_to_analytics
  -  docker run test-univ_db_report_to_csv
  
or can re-run container in docker desktop for the pipeline
<img width="1267" alt="image" src="https://user-images.githubusercontent.com/42090252/163711457-a7cf6d7b-3096-46a4-a887-4ac1813160e6.png">



<img width="737" alt="image" src="https://user-images.githubusercontent.com/42090252/163710979-e1aa4213-10eb-42a4-893a-c7de0d3fa933.png">



and make sure the cointainer status already running and Exited (0) -> for the cointainer run python script for ingestion with cmd : **docker container ls -a**__
