FROM python:latest
WORKDIR /code
ADD ./app/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY ./app/config.py config.py
COPY ./app/dataset_to_analytics.py dataset_to_analytics.py
CMD ["python3", "-u", "dataset_to_analytics.py"]