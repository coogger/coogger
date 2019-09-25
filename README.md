<h1 align="center">COOGGER PROJECT</h1>
Coogger is a platform for developers to publish technical documents in the best way.
 
[![MIT License](https://img.shields.io/github/license/coogger/coogger.svg)](https://github.com/coogger/coogger/blob/super-coogger/LICENSE.txt) [![releases](https://img.shields.io/github/release/coogger/coogger.svg)](https://github.com/coogger/coogger/releases) [![last-commit](https://img.shields.io/github/last-commit/coogger/coogger.svg)](https://github.com/coogger/coogger/commits/master) [![Codacy Badge](https://img.shields.io/codacy/grade/56b6c891028543d685564b78ab3431d2)](https://www.codacy.com/app/hakancelik96/coogger?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=coogger/coogger&amp;utm_campaign=Badge_Grade) [![style](https://img.shields.io/badge/style-black-black)](https://github.com/psf/black) [![style](https://img.shields.io/badge/style-isort-lightgrey)](https://github.com/timothycrosley/isort) [![style](https://img.shields.io/badge/style-unimport-green)](https://github.com/hakancelik96/unimport) [![](https://img.shields.io/github/contributors/coogger/coogger)](https://github.com/coogger/coogger/graphs/contributors)

------------------------

**Please insert this badge into readme.md of your repo which uses this project.**

 ` [![docs coogger](https://img.shields.io/badge/docs-coogger-1c472b)](https://github.com/coogger/coogger)`
 
 [![docs coogger](https://img.shields.io/badge/docs-coogger-1c472b)](https://github.com/coogger/coogger)
 
 ------------------------

### 🚀 Installation 🚀
#### Before

`git clone https://github.com/coogger/coogger.git`

Create .env file like below
**/coogger/coogger/.env**

```
DEBUG=on
SECRET_KEY=your_django_app_secret_key

DEFAULT_DB_NAME=default_db_name_or_path
DJANGO_IP_DB_NAME=django_ip_db_name_or_path
COOGGER_IMAGES_DB_NAME=cooggerimages_db_name_or_path
REDIRECT_DB_NAME==redirect_db_name_or_path

GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret

EMAIL_PASSWORD=******
```

##### After

```shell
$ pip install -r requirements.txt
$ python manage.py makemigrations django_follow_system
$ python manage.py makemigrations cooggerimages
$ python manage.py makemigrations django_page_views
$ python manage.py makemigrations djangoip
$ python manage.py makemigrations django_vote_system

$ python manage.py migrate --database default
$ python manage.py migrate --database django_ip
$ python manage.py migrate --database coogger_images
$ python manage.py migrate --database redirect
$ python manage.py runserver
```

##### Docker
```
$ docker-compose up --env-file coogger/.env
```

## 🤝 Contributing 🤝
[CONTRIBUTING.md](https://github.com/coogger/coogger/blob/coogger-dev/CONTRIBUTING.md)

## Author / Social

👤 **Hakan Çelik** 👤

- [![](https://img.shields.io/twitter/follow/hakancelik96?style=social)](https://twitter.com/hakancelik96)
- [![](https://img.shields.io/twitter/follow/cooggercom?style=social)](https://twitter.com/cooggercom)
- [![](https://img.shields.io/github/followers/hakancelik96?label=hakancelik96&style=social)](https://github.com/hakancelik96)