Task:
Hi there! Your 3rd task is: rewrite your 1st lab to use some kind of database to store crawled data (MySQL, MongoDB, Elasticsearch and so on). Database you gonna use have to be packed up inside Docker container and you have to use docker-compose to run it near your app!

This repo creates 2 docker images - redis and flask by docker-compose.
Then flask makes crawling.

Instruction:
1) create images
docker-compose build --no-cache
2) run images
docker-compose up
3) visit url
http://localhost:5000/
4) see result

Backend:
1) visit urls from urls.txt
2) search words from search_query.txt
3) save result to redis database
4) load result from redis on page refresh

Help:
https://docs.docker.com/compose/gettingstarted/

![application](https://github.com/andreipit/cloud_computing_hw1_parser/blob/main/video.gif)




