FROM debian:bullseye-slim

RUN apt-get update && apt-get upgrade && apt-get install -y\
    python3-pip

ADD run.py .

RUN pip install yeelight paho-mqtt

CMD ["python3", "-u", "/run.py"]]