FROM python:latest
WORKDIR /code
ADD ./app/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY ./app/config.py config.py
COPY ./app/source_to_raw_layer.py source_to_raw_layer.py
CMD ["python3", "-u", "source_to_raw_layer.py"]