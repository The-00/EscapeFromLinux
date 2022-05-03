FROM ubuntu:20.04

RUN apt-get update && apt-get install -y --no-install-recommends python3.5 python3-pip && \
    apt-get clean 

RUN pip install --no-cache-dir --upgrade pip &&\
    pip install --no-cache-dir fastapi uvicorn

COPY brain/ /srv/EFL
COPY exos/  /srv/EFL/exos

WORKDIR /srv/EFL
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "80"]