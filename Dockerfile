FROM python:3.6

RUN \
    export http_proxy=http://company.proxy.com:port \
    && apt-get update -y && apt-get upgrade -y \
    && apt-get install -y sqlite3 libsqlite3-dev

WORKDIR /deployment

ENV PYTHONUNBUFFERED 1

COPY requirements.txt .
RUN pip install -r requirements.txt --proxy="company.proxy.com:port"

# copy project
COPY . .

RUN python ./manage.py makemigrations
RUN python ./manage.py migrate
RUN cat import.sql | sqlite3 db.sqlite3
EXPOSE 8000
CMD [ "python", "./manage.py", "runserver", "0.0.0.0:8000" ]

