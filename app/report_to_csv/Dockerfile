FROM python:latest
WORKDIR /code
ADD ./app/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY ./app/config.py config.py
COPY ./app/data_to_csv.py data_to_csv.py
CMD ["python3", "-u", "data_to_csv.py"]