FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
RUN python manage.py makemigrations cooggerapp
RUN python manage.py makemigrations django_ban
RUN python manage.py migrate --database default
RUN python manage.py migrate --database django_ban
