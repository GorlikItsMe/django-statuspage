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

## Testing

```sh
flake8
pytest --cov --cov-report html
python manage.py test
```

## Setup with nginx

```sh
pip install gunicorn psycopg2
sudo nano /etc/systemd/system/gunicorn_statuspage.service
```

```
[Unit]
Description=gunicorn_statuspage daemon
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/django-statuspage
# EnvironmentFile=/var/www/django-statuspage/.env
ExecStart=/var/www/django-statuspage/.venv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/var/www/django-statuspage/djstatuspage.sock djstatuspage.wsgi:application

[Install]
WantedBy=multi-user.target

```

```sh
sudo systemctl start gunicorn_statuspage
sudo systemctl enable gunicorn_statuspage
sudo systemctl status gunicorn_statuspage
# If error check djstatuspage.sock permissions, maybe it cant create
chown www-data:www-data /var/www/django-statuspage
sudo systemctl restart gunicorn_statuspage
```

Ngnix config

```
server {
    listen 80;
    server_name status.domain.com;

    gzip on;
    error_log /var/log/nginx/status_error.log warn;
    access_log /var/log/nginx/status_access.log;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        alias /var/www/django-statuspage/staticfiles/; # ending slash is required
    }
    location /media/ {
        alias /var/www/django-statuspage/media/; # ending slash is required
    }
    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/django-statuspage/djstatuspage.sock;
    }
}
```

```
sudo ln -s /etc/nginx/sites-available/myproject /etc/nginx/sites-enabled
```
 