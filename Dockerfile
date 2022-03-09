FROM ubuntu:20.04

ARG API_KEY

ENV TOKEN $API_KEY

WORKDIR /stocktracker

ADD . /stocktracker

RUN apt-get update && \
    apt-get install -y --no-install-recommends python3-pip build-essential python3-dev libssl-dev libffi-dev iputils-ping vim jq && \
    apt-get clean && rm -rf /var/lib/apt/lists/* && \
    useradd stocks && \
    usermod -aG stocks && \
    pip3 install --no-cache-dir -r requirements.txt && \
    python3 /stocktracker/setup.py install

USER stocks

CMD ["python3", "stocktracker.py"]