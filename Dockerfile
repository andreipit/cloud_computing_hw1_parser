FROM python:3.8-slim

WORKDIR /code
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

#RUN uname -r
RUN apt update -y
RUN apt-get update -y
RUN apt-get upgrade -y
#RUN apt-get install linux-headers-2.6-2.6.32-5-amd64

#RUN apt install linux-headers -y

RUN apt install -y build-essential
RUN apt-get install -y manpages-dev
RUN apt-get install -y musl-dev

RUN pip install --no-cache-dir pandas numpy

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

EXPOSE 5000
COPY . .
CMD ["flask", "run"]
#CMD ["python", "-m", "flask", "run"]