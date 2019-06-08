[![MIT License](https://img.shields.io/github/license/coogger/coogger.svg?style=for-the-badge)](https://github.com/coogger/coogger/blob/super-coogger/LICENSE.txt) [![](https://img.shields.io/github/release/coogger/coogger.svg?style=for-the-badge)](https://github.com/coogger/coogger/releases) ![](https://img.shields.io/github/last-commit/coogger/coogger.svg?style=for-the-badge) [![](https://img.shields.io/discord/465599004865200129.svg?label=Discord&style=for-the-badge)](https://discord.gg/avmdZJa)

### How to run coogger in my computer?

#### Before
**/coogger/coogger/.env**

```
DEBUG=on
SECRET_KEY=your_django_app_secret_key

DEFAULT_DB_NAME=default_db_name_or_path
DJANGO_IP_DB_NAME=django_ip_db_name_or_path
COOGGER_IMAGES_DB_NAME=cooggerimages_db_name_or_path

GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret

EMAIL_PASSWORD=*******
```

##### After

```python
>>> pip install -r requirements.txt
>>> python manage.py makemigrations cooggerapp
# >>> python manage.py makemigrations github_auth
# >>> python manage.py makemigrations django_follow_system
# >>> python manage.py makemigrations cooggerimages
# >>> python manage.py makemigrations django_page_views
# >>> python manage.py makemigrations djangoip
# >>> python manage.py makemigrations django_ban
# >>> python manage.py makemigrations django_vote_system

>>> python manage.py migrate --database default
>>> python manage.py migrate --database django_ip
>>> python manage.py migrate --database coogger_images
>>> python manage.py runserver
```

##### Docker
```
$ docker-compose up --env-file coogger/.env
```

#### [More Information - About coogger](https://www.coogger.com/about/@coogger)
