# FROM python:3.9

# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# WORKDIR /code

# COPY requirements.txt /code/
# RUN pip install -r requirements.txt
# RUN pip install psycopg2-binary django-prometheus locust
# COPY . /code/