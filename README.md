    [![MIT License](https://img.shields.io/github/license/coogger/coogger.svg?style=for-the-badge)](https://github.com/coogger/coogger/blob/super-coogger/LICENSE.txt) [![](https://img.shields.io/github/release/coogger/coogger.svg?style=for-the-badge)](https://github.com/coogger/coogger/releases) ![](https://img.shields.io/github/last-commit/coogger/coogger.svg?style=for-the-badge) [![](https://img.shields.io/discord/465599004865200129.svg?label=Discord&style=for-the-badge)](https://discord.gg/avmdZJa)


    ### How to run coogger in my computer?

    #### Before
    **/coogger/coogger/.env**

    ```
    DEBUG=on
    SECRET_KEY=django_secret_key
    CLIENT_ID=your_steem_app_name
    APP_SECRET=your_steemconnect_app_key
    DEFAULT_DB_NAME=path/to/default_db.db
    DJANGO_BAN_DB_NAME=path/to/django_ban.db
    COOGGER_IMAGES_DB_NAME=path/to/coogger_images.db
    ```

    ##### After

    ```python
    >>> pip install -r requirements.txt
    >>> python manage.py makemigrations cooggerapp
    >>> python manage.py makemigrations django_ban
    >>> python manage.py makemigrations cooggerimages
    >>> python manage.py migrate --database default
    >>> python manage.py migrate --database django_ban
    >>> python manage.py migrate --database coogger_images
    >>> python manage.py runserver
    ```

    ##### Docker
    ```
    $ docker-compose up --env-file coogger/.env
    ```

    #### [More Information - About coogger](https://www.coogger.com/about/@coogger)
