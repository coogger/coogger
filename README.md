<h1 align="center">COOGGER PROJECT</h1>
<p align="left">
  Coogger is a platform where developers can write their knowledge, experience, documentation and blogs.
 </p>
<p align="center">
  <a href="https://github.com/coogger/coogger/blob/super-coogger/LICENSE.txt" target="_blank">
    <img alt="MIT License" title="MIT License" src="https://img.shields.io/github/license/coogger/coogger.svg?style=for-the-badge"/>
  </a>
  <a href="https://github.com/coogger/coogger/releases" target="_blank">
    <img alt="releases" title="releases" src="https://img.shields.io/github/release/coogger/coogger.svg?style=for-the-badge"/>
  </a>
  <img alt="last-commit" title="last-commit" src="https://img.shields.io/github/last-commit/coogger/coogger.svg?style=for-the-badge"/>
 <a href="https://discord.gg/avmdZJa" target="_blank">
    <img alt="releases" title="releases" src="https://img.shields.io/discord/465599004865200129.svg?label=Discord&style=for-the-badge"/>
  </a>
</p>
<h2 align="center">WHAT IS COOGGER</h2>

### 🚀 Installation
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

## 🤝 Contributing

Contributions, issues and feature requests are welcome.<br />
Feel free to check [issues page](https://github.com/coogger/coogger/issues) if you want to contribute.

## Contributors

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore -->
<table>
  <tr>
    <td align="center">
      <a href="https://github.com/isidentical">
        <img src="https://avatars3.githubusercontent.com/u/47358913?s=460&v=4" width="75px;" alt="Batuhan Taşkaya"/>
        <br/>
        <sub>
          <b>Batuhan Taşkaya</b>
        </sub>
      </a>
      <br/>
      <a href="https://github.com/coogger/coogger/commits?author=isidentical" title="Code">💻</a>
      <a href="https://github.com/coogger/coogger/issues?q=author%3Aisidentical" title="Bug reports">🐛</a>
    </td>
    <td align="center">
      <a href="https://github.com/furkanonder">
        <img src="https://avatars0.githubusercontent.com/u/24194934?s=460&v=4" width="75px;" alt="Furkan Önder"/>
        <br/>
        <sub>
          <b>Furkan Önder</b>
        </sub>
      </a>
      <br/>
      <a href="https://github.com/coogger/coogger/commits?author=furkanonder" title="Code">💻</a>
      <a href="https://github.com/coogger/coogger/commits?author=furkanonder" title="Documentation">📖</a>
    </td>
    <td align="center">
      <a href="https://github.com/Yutyo">
        <img src="https://avatars2.githubusercontent.com/u/40173707?s=460&v=4" width="75px;" alt="Yutyo"/>
        <br/>
        <sub>
          <b>Yutyo</b>
        </sub>
      </a>
      <br/>
      <a href="https://github.com/coogger/coogger/commits?author=Yutyo" title="Documentation">📖</a>
      <a href="https://github.com/coogger/coogger/issues?q=author%3AYutyo" title="Bug reports">🐛</a>
    </td>
    <td align="center">
      <a href="https://github.com/adilkhan8000">
        <img src="https://avatars0.githubusercontent.com/u/37472106?s=460&v=4" width="75px;" alt="alishannoor"/>
        <br/>
        <sub>
          <b>alishannoor</b>
        </sub>
      </a>
      <br/>
      <a href="https://github.com/coogger/coogger/commits?author=adilkhan8000" title="Documentation">📖</a>
      <a href="https://github.com/coogger/coogger/issues?q=author%3Aadilkhan8000" title="Bug reports">🐛</a>
    </td>
    <td align="center">
      <a href="https://github.com/ewuoso">
        <img src="https://avatars2.githubusercontent.com/u/33087808?s=460&v=4" width="75px;" alt="ewuoso"/>
        <br/>
        <sub>
          <b>ewuoso</b>
        </sub>
      </a>
      <br/>
      <a href="https://github.com/coogger/coogger/commits?author=ewuoso" title="Documentation">📖</a>
      <a href="https://github.com/coogger/coogger/issues?q=author%3Aewuoso" title="Bug reports">🐛</a>
    </td>
  </tr>
</table>

<!-- ALL-CONTRIBUTORS-LIST:END -->

## Author

👤 **Hakan Çelik**

- Twitter: [@hakancelik_py](https://twitter.com/hakancelik_py)
- Twitter: [@cooggercom](https://twitter.com/cooggercom)
- Github: [@hakancelik96](https://github.com/hakancelik96)

## 📝 License

Copyright © 2019 [Hakan Çelik](https://github.com/coogger/coogger).<br/>
This project is [MIT](https://github.com/coogger/coogger/blob/master/LICENSE) licensed.
