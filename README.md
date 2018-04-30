[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/coogger/blob/master/LICENSE.txt)
[![Coogger channel on Discord](https://img.shields.io/badge/chat-discord-738bd7.svg)](https://discord.gg/kJMbsdT)

## What is coogger ?

coogger is an information sharing network that works with [multiple applications](http://www.coogger.com/apps) the network web front-end to the Steem Blockchain http://www.coogger.com

-----

### Usage

- pip install -r requirements.txt

```python
python manage.py makemigrations
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
