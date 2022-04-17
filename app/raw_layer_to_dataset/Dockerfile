FROM python:latest
WORKDIR /code
ADD ./app/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY ./app/config.py config.py
COPY ./app/raw_layer_to_dataset.py raw_layer_to_dataset.py
CMD ["python3", "-u", "raw_layer_to_dataset.py"]