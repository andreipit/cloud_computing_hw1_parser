# syntax=docker/dockerfile:1
# FROM python:3.7-alpine
FROM python:3.7.6-buster
RUN pip install pandas==1.0.0

WORKDIR /code
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
# fixes bug: ERROR: Failed building wheel for numpy, python3.9 also helps
RUN pip install numpy==1.19.5
# RUN pip install pandas==1.1.5
RUN pip install -r requirements.txt
EXPOSE 5000
COPY . .
CMD ["flask", "run"]