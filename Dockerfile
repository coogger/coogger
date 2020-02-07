FROM python:3.7.5
ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code

RUN pip install pipenv
COPY Pipfile /code/
COPY Pipfile.lock /code/
RUN pipenv install --system --dev
COPY . /code/

RUN python manage.py migrate
