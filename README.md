[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/coogger/blob/master/LICENSE.txt)
[![Coogger channel on Discord](https://img.shields.io/badge/chat-discord-738bd7.svg)](https://discord.gg/kJMbsdT)
[instagram page](https://www.instagram.com/coogger.v1/)
[Facebook page](https://www.facebook.com/coogger)

Coogger is an Open Source social information sharing network that works with [multiple applications](http://www.coogger.com/apps)
and coogger rewards these information shares.

====================

### Usage

- pip install -r requirements.txt

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
