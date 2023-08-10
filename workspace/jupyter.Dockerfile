FROM phidata/jupyter:4.0.2

COPY requirements.txt /
RUN pip install -r /requirements.txt
