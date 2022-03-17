# syntax=docker/dockerfile:1
FROM python:3.7-alpine
WORKDIR /code
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
# fixes bug: ERROR: Failed building wheel for numpy
RUN pip install numpy
RUN pip install pandas
RUN pip install -r requirements.txt
EXPOSE 5000
COPY . .
CMD ["flask", "run"]