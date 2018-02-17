[![Licence](https://img.shields.io/github/license/mashape/apistatus.svg)](https://github.com/hakancelik96/coogger/blob/master/LICENSE.txt)

coogger is an information sharing network that works with multiple applications
[apps](http://www.coogger.com/apps)
====================

+ coogger.com, the information sharing platform, is currently available only in Turkish
+ follow us or join us
  - [instagram page](https://www.instagram.com/coogger.v1/)
  - [Facebook page](https://www.facebook.com/coogger)

before
-
- pip install -r requirements.txt

Use as follows
-------

```python
python manage.py migrate --database=steemit
python manage.py migrate --database=default
python manage.py makemigrations steemitapp
python manage.py makemigrations cooggerapp
python manage.py migrate
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
