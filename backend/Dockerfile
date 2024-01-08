FROM tensorflow/tensorflow:latest-gpu

ADD . /app

WORKDIR /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt  --ignore-installed blinker
CMD python index.py