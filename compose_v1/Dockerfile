FROM ubuntu:18.04

RUN apt-get -y update
RUN apt-get install -y git
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN pip3 install --upgrade pip
RUN cd home
RUN git clone https://github.com/andreipit/cloud_computing_hw1_parser
RUN cd cloud_computing_hw1_parser
RUN pip install -r requirements.txt
# RUN echo 'Hello World from Docker!' > /var/www/html/index.html

EXPOSE 5000
