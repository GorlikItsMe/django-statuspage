# Django StatusPage

Its page what will check your services is online or not

## Setup

```sh
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

After that start

```sh
python manage.py check_status
```

There are executed all checks of services. It should run if you want check services status.
