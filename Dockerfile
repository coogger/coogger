FROM python:3-onbuild

WORKDIR .

RUN pip install --trusted-host pypi.python.org -r requirements.txt

ENTRYPOINT ["python"]
CMD ["manage.py","migrate"]
CMD ["manage.py","makemigrations","cooggerapp"]
CMD ["manage.py","runserver"]

EXPOSE 8000

ENV NAME coogger
