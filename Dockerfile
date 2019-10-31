FROM python:3.7.5
ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code

RUN pip install pipenv
COPY Pipfile /code/
COPY Pipfile.lock /code/
RUN pipenv install --system --dev
COPY . /code/

RUN python manage.py makemigrations cooggerapp
RUN python manage.py makemigrations django_follow_system
RUN python manage.py makemigrations cooggerimages
RUN python manage.py makemigrations django_page_views
RUN python manage.py makemigrations djangoip
RUN python manage.py makemigrations django_vote_system

RUN python manage.py migrate --database default
RUN python manage.py migrate --database django_ip
RUN python manage.py migrate --database coogger_images
RUN python manage.py migrate --database redirect
