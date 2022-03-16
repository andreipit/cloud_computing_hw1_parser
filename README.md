Task:
Hi there! Your 3rd task is: rewrite your 1st lab to use some kind of database to store crawled data (MySQL, MongoDB, Elasticsearch and so on). Database you gonna use have to be packed up inside Docker container and you have to use docker-compose to run it near your app!


1) interactive way (jupyter notebook):
docker run -v "%cd%":/tmp/working -w=/tmp/working -p 8888:8888 --rm -it jupyter/datascience-notebook:8c2836ace4a1 jupyter notebook --no-browser --ip="*" --notebook-dir=/tmp/working --allow-root   

2) classic way (conda):
conda create -n grasp_env python=3.6
pip install -r requirements.txt
python mini_google.py

3) dockerfile way:
cd <Dockerfile location>
docker build -f ./Dockerfile -t developing/img03:tag01 .
docker run -it --rm developing/img03:tag01
cd cloud_computing_hw1_parser

pip install -r -requirements.txt

