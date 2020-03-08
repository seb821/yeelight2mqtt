FROM debian:stretch

RUN apt-get update && apt-get install -y\
    python-pip

COPY . ./

RUN pip install -r requirements.txt

CMD ["python", "-u", "/run.py"]]

