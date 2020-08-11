<h1 align="center">COOGGER PROJECT</h1>
Coogger is a platform for developers to publish technical documents in the best way.

[![MIT License](https://img.shields.io/github/license/coogger/coogger.svg)](https://github.com/coogger/coogger/blob/super-coogger/LICENSE.txt)
[![releases](https://img.shields.io/github/release/coogger/coogger.svg)](https://github.com/coogger/coogger/releases)
[![last-commit](https://img.shields.io/github/last-commit/coogger/coogger.svg)](https://github.com/coogger/coogger/commits/master)
[![style](https://img.shields.io/badge/style-black-black)](https://github.com/psf/black)
[![style](https://img.shields.io/badge/style-isort-lightgrey)](https://github.com/timothycrosley/isort)
[![style](https://img.shields.io/badge/style-unimport-green)](https://github.com/hakancelik96/unimport)
[![](https://img.shields.io/github/contributors/coogger/coogger)](https://github.com/coogger/coogger/graphs/contributors)

---

**Please insert this badge into readme.md of your repo which uses this project.**

`[![docs coogger](https://img.shields.io/badge/docs-coogger-1c472b)](https://github.com/coogger/coogger)`

[![docs coogger](https://img.shields.io/badge/docs-coogger-1c472b)](https://github.com/coogger/coogger)

---

### 🚀 Installation 🚀

#### Before

`git clone https://github.com/coogger/coogger.git`

Create .env file like below **/coogger/coogger/.env**

```
DEBUG=on
SECRET_KEY=your_django_app_secret_key

DEFAULT_DB_NAME=default_db_name_or_path

GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret

EMAIL_PASSWORD=******
```

##### After

```shell
$ pip3.8 install virtualenv
$ python3.8 -m venv env
$ source env/bin/activate
$ pip3.8 install -r requirements.txt
$ python manage.py migrate
$ python manage.py create_ghost_user
$ python manage.py runserver
```

**Multiple languages**

```shell
python manage.py makemessages -l tr
python manage.py compilemessages
```

##### Docker

```
$ docker-compose up --env-file coogger/.env
```

## 🤝 Contributing 🤝

[CONTRIBUTING.md](https://github.com/coogger/coogger/blob/coogger-dev/CONTRIBUTING.md)

[![](https://sourcerer.io/fame/hakancelik96/coogger/coogger/images/0)](https://sourcerer.io/fame/hakancelik96/coogger/coogger/links/0)[![](https://sourcerer.io/fame/hakancelik96/coogger/coogger/images/1)](https://sourcerer.io/fame/hakancelik96/coogger/coogger/links/1)[![](https://sourcerer.io/fame/hakancelik96/coogger/coogger/images/2)](https://sourcerer.io/fame/hakancelik96/coogger/coogger/links/2)[![](https://sourcerer.io/fame/hakancelik96/coogger/coogger/images/3)](https://sourcerer.io/fame/hakancelik96/coogger/coogger/links/3)[![](https://sourcerer.io/fame/hakancelik96/coogger/coogger/images/4)](https://sourcerer.io/fame/hakancelik96/coogger/coogger/links/4)[![](https://sourcerer.io/fame/hakancelik96/coogger/coogger/images/5)](https://sourcerer.io/fame/hakancelik96/coogger/coogger/links/5)[![](https://sourcerer.io/fame/hakancelik96/coogger/coogger/images/6)](https://sourcerer.io/fame/hakancelik96/coogger/coogger/links/6)[![](https://sourcerer.io/fame/hakancelik96/coogger/coogger/images/7)](https://sourcerer.io/fame/hakancelik96/coogger/coogger/links/7)

## Author / Social

👤 **Hakan Çelik** 👤

- [![](https://img.shields.io/twitter/follow/hakancelik96?style=social)](https://twitter.com/hakancelik96)
- [![](https://img.shields.io/twitter/follow/cooggercom?style=social)](https://twitter.com/cooggercom)
- [![](https://img.shields.io/github/followers/hakancelik96?label=hakancelik96&style=social)](https://github.com/hakancelik96)
