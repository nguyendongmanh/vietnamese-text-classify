FROM python:3.11.6-slim

WORKDIR /app

RUN python -m pip install --upgrade pip

COPY requirements.txt /app/

RUN pip install -r requirements.txt

RUN mkdir data

COPY . /app/

CMD [ "python", "src/run_crawl.py"]