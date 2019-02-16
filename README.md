[![MIT License](https://img.shields.io/github/license/coogger/coogger.svg?style=for-the-badge)](https://github.com/coogger/coogger/blob/super-coogger/LICENSE.txt) [![](https://img.shields.io/github/release/coogger/coogger.svg?style=for-the-badge)](https://github.com/coogger/coogger/releases) ![](https://img.shields.io/website-up-down-green-red/https/www.coogger.com.svg?style=for-the-badge)

 ![](https://img.shields.io/github/watchers/coogger/coogger.svg?style=for-the-badge) ![](https://img.shields.io/github/stars/coogger/coogger.svg?style=for-the-badge) ![](https://img.shields.io/github/forks/coogger/coogger.svg?label=Fork&style=for-the-badge)

![](https://img.shields.io/github/last-commit/coogger/coogger.svg?style=for-the-badge)

![](https://img.shields.io/github/issues/coogger/coogger.svg?style=for-the-badge) ![](https://img.shields.io/github/issues-pr/coogger/coogger.svg?style=for-the-badge)

![](https://img.shields.io/github/languages/code-size/coogger/coogger.svg?style=for-the-badge) ![](https://img.shields.io/github/languages/top/coogger/coogger.svg?style=for-the-badge) ![](https://img.shields.io/github/languages/count/coogger/coogger.svg?style=for-the-badge)

[![](https://img.shields.io/discord/465599004865200129.svg?label=Discord&style=for-the-badge)](https://discord.gg/avmdZJa)


### How to run coogger in my computer?

#### Before
**/coogger/coogger/.env**

```
DEBUG=on
SECRET_KEY=django_secret_key
DATABASES_ENGINE=django.db.backends.sqlite3
DATABASES_NAME=coogger.db
CLIENT_ID=your_steem_app_name
APP_SECRET=your_steemconnect_app_key
```

##### After

```python
>>> pip install -r requirements.txt
>>> python manage.py makemigrations cooggerapp
>>> python manage.py migrate
>>> python manage.py runserver
```

#### [More Information - About coogger](https://www.coogger.com/about/@coogger)
