[![Licence](https://img.shields.io/github/license/mashape/apistatus.svg)](https://github.com/hakancelik96/coogger/blob/master/LICENSE.txt)

coogger - is information sharing platform
====================
coogger.com, the information sharing platform, is currently available only in Turkish
-

[![web site](http://www.coogger.com/static/media/favicon.png)](http://www.coogger.com)

before
-
- pip install -r requirements.txt

Use as follows
-------

```python
python manage.py migrate

python manage.py makemigrations cooggerapp

python manage.py runserver

```

---
### Docker Usage
Build it:
```
$ docker build -t username/coogger .
```

Run it:
```
$ docker run -it -p 8000:8000 username/coogger
```
---


[To-do](https://github.com/hakancelik96/coogger/projects/1)
[Contribution guidelines for this project](#)
[CODE OF CONDUCT](#)
